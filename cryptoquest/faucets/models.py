import json
from decimal import Decimal

from django.db import models
from django.conf import settings

from channels import Group


class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=40, decimal_places=30, blank=True, null=True)
    lng = models.DecimalField(max_digits=40, decimal_places=30, blank=True, null=True)

    def __str__(self):
        return self.name


class Faucet(models.Model):
    location = models.ForeignKey('Location', related_name='faucets', on_delete=models.CASCADE)
    coin = models.ForeignKey('coins.Coin', related_name='coins', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} - {self.coin}'


class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sessions', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', related_name='sessions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} - {self.user}'

    def save(self, *args, **kwargs):
        is_new = not self.pk

        super().save(*args, **kwargs)

        if is_new:
            Group('cryptoquest').send({
                'text': json.dumps({
                    'type': 'session_started',
                    'data': {
                        'user': {
                            'first_name': self.user.first_name,
                            'last_name': self.user.last_name,
                        }
                    }
                })
            })


class CoinSpawn(models.Model):
    faucet = models.ForeignKey('Faucet', related_name='spawns', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=40, decimal_places=20)
    type = models.CharField(
        max_length=20,
        choices=(
            ('coin', 'Coin'),
            ('boss', 'Boss'),
        ),
        default='coin'
    )
    state = models.CharField(
        max_length=20,
        choices=(
            ('spawned', 'Spawned'),
            ('captured', 'Captured'),
        )
    )
    health = models.IntegerField(default=1)
    captured_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captured_coin_spawns', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        from ..serializers import CoinSpawnSerializer
        from ..wallets.models import Wallet

        is_new = not self.pk
        is_new_capture = False

        if not is_new:
            if self.health == 0:
                is_new_capture = True
                self.state = 'captured'

        super().save(*args, **kwargs)

        if is_new:
            if self.type == 'boss':
                Group('cryptoquest').send({
                    'text': json.dumps({
                        'type': 'shitcoin',
                        'data': {}
                    })
                })
            else:
                serializer = CoinSpawnSerializer(self)
                Group('cryptoquest').send({
                    'text': json.dumps({
                        'type': 'spawn_new',
                        'data': {
                            'spawn': serializer.data
                        }
                    })
                })

        if is_new_capture:
            wallet, _ = Wallet.objects.get_or_create(
                user=self.captured_by,
                coin=self.faucet.coin,
                defaults={
                    'balance': Decimal(0)
                }
            )
            wallet.balance += self.amount
            wallet.save()
            Group('cryptoquest').send({
                'text': json.dumps({
                    'type': 'spawn_captured',
                    'data': {
                        'spawn': CoinSpawnSerializer(self).data
                    }
                })
            })
