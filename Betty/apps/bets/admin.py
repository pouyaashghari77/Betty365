from django.contrib import admin
from import_export.admin import ImportMixin
from import_export.resources import ModelResource

from Betty.apps.bets.models import Bet, Event, Deposit


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'home', 'away', 'date', 'result']
    list_filter = ['date', 'result']
    list_editable = ['result']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['event', 'selection', 'side', 'stake', 'odds', 'matched', 'has_won']
    list_filter = ['matched', 'has_won']
    list_editable = ['has_won']


class DepositResource(ModelResource):
    class Meta:
        model = Deposit
        import_id_fields = []
        fields = ('serial_num', 'code', 'value')


@admin.register(Deposit)
class DepositAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = DepositResource
    list_display = ['serial_num', 'code', 'value', 'created', 'updated']
