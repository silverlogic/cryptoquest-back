import os

from coinbase.wallet.client import Client
from rest_framework import viewsets, mixins, decorators, generics, response

from .faucets.models import Location, CoinSpawn
from .serializers import LocationSerializer, CoinSpawnSerializer


class LocationsViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class CoinSpawnsViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CoinSpawnSerializer
    queryset = CoinSpawn.objects.filter(state='spawned')


class ReceiveView(generics.GenericAPIView):
    def post(self, request):
        client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SECRET'])
        address = client.create_address('5d049360-410b-50e9-aef4-60b37e42d79e')  # create btc wallet address
        return response.Response({'address': address.address}, status=201)


class ShitAttackView(generics.GenericAPIView):
    def post(self, request):
        CoinSpawn.objects.filter(faucet__coin__name='Shitcoin').delete()
        CoinSpawn.objects.create(
            faucet_id=6,
            amount=1,
            type='boss',
            state='spawned',
            health=9
        )
