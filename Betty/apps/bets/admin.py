from django.contrib import admin

from Betty.apps.bets.models import Bet, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'home', 'away', 'date', 'sport_name', 'league', 'match_result']
    list_filter = ['sport_name', 'date', 'match_result']
    list_editable = ['match_result']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['event', 'selection', 'side', 'stake', 'odds', 'matched', 'has_won']
    list_filter = ['matched', 'has_won']
    list_editable = ['has_won']
