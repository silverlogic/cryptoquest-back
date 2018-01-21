from django.contrib import admin

from .models import Coin


class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Coin, CoinAdmin)
