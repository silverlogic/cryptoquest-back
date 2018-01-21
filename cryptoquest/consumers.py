import json

from django.contrib.auth import get_user_model

from channels import Group

from .faucets.models import CoinSpawn, Faucet, Session
from .serializers import CoinSpawnSerializer



def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('cryptoquest').add(message.reply_channel)
    spawns = CoinSpawn.objects.filter(state='spawned')
    serializer = CoinSpawnSerializer(spawns, many=True)
    message.reply_channel.send({
        'text': json.dumps({
            'type': 'spawn_list',
            'data': {
                'spawns': serializer.data
            }
        })
    });


def ws_disconnect(message):
    Group('cryptoquest').discard(message.reply_channel)


def ws_message(message):
    print(message['text'])
    event_info = json.loads(message['text'])
    event_type = event_info['type']
    event_data = event_info['data']
    if event_type == 'shoot':
        coin_spawn = CoinSpawn.objects.select_for_update().get(pk=event_data['spawn_id'])
        if coin_spawn.state != 'spawned':
            return
        coin_spawn.health -= 1
        if coin_spawn.health == 0:
            coin_spawn.captured_by = get_user_model().objects.get(pk=event_data['user_id'])
        coin_spawn.save()
    elif event_type == 'spawn_add':
        CoinSpawn.objects.create(
            faucet=Faucet.objects.get(pk=7),
            amount=1,
            state='spawned',
        )
    elif event_type == 'session_start':
        Session.objects.create(
            user_id=event_data['user_id'],
            location_id=1
        )
    elif event_type == 'shitcoin':
        CoinSpawn.objects.filter(faucet__coin__name='Shitcoin').delete()
        CoinSpawn.objects.create(
            faucet_id=6,
            amount=1,
            type='boss',
            state='spawned',
            health=9
        )
    elif event_type == 'balance_update':
        Group('cryptoquest').send({
            'text': json.dumps({
                'type': 'balance_updated',
                'data': {}
            })
        })
