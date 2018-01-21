from django.contrib import admin

from .models import Location, Faucet, CoinSpawn, Session


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class FaucetAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'coin',)


class CoinSpawnAdmin(admin.ModelAdmin):
    list_display = ('id', 'faucet', 'amount', 'state', 'captured_by',)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location')


admin.site.register(Location, LocationAdmin)
admin.site.register(Faucet, FaucetAdmin)
admin.site.register(CoinSpawn, CoinSpawnAdmin)
admin.site.register(Session, SessionAdmin)
