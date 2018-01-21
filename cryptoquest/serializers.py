from rest_framework import serializers

from .coins.models import Coin
from .faucets.models import Faucet, Location, CoinSpawn


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('id', 'name', 'logo',)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'lat', 'lng')


class FaucetSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    coin = CoinSerializer()

    class Meta:
        model = Location
        fields = ('id', 'coin', 'location')


class CoinSpawnSerializer(serializers.ModelSerializer):
    faucet = FaucetSerializer()

    class Meta:
        model = CoinSpawn
        fields = ('id', 'faucet', 'type', 'amount', 'captured_by',)
