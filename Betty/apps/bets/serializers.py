from rest_framework import serializers

from Betty.apps.bets.models import Bet
from Betty.apps.events.serializers import ShortEventSerializer


class PlaceBetsSerializer(serializers.Serializer):
    SIDE_CHOICES = (
        ('Back', 'Back'),
        ('Lay', 'Lay'),
    )

    SELECTION_CHOICES = (
        ('Home', 'Home'),
        ('Away', 'Away')
    )

    selection = serializers.ChoiceField(choices=SELECTION_CHOICES)
    side = serializers.ChoiceField(choices=SIDE_CHOICES)
    odds = serializers.FloatField()
    stake = serializers.FloatField()

    def create(self, validated_data):
        event = self.context.get('event')
        user = self.context.get('user')
        return Bet.objects.create(
            event=event, user=user,
            **validated_data
        )


class UserBetsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    event = ShortEventSerializer()
    selection = serializers.CharField()
    side = serializers.CharField()
    odds = serializers.FloatField()
    stake = serializers.FloatField()
    matched = serializers.BooleanField()
    has_won = serializers.NullBooleanField()
