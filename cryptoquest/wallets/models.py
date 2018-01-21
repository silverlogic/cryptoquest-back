from django.conf import settings
from django.db import models


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wallets', on_delete=models.CASCADE)
    coin = models.ForeignKey('coins.Coin', related_name='wallets', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=40, decimal_places=20)

    def __str__(self):
        return f'{self.user} - {self.coin} - {self.balance}'
