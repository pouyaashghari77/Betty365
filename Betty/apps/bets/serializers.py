from rest_framework import serializers

from Betty.apps.bets.models import Bet, Event


class EventsRequestSerializer(serializers.Serializer):
    sport_name = serializers.CharField(required=False, default='')


class EventsResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['external_id']


class ShortEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    home = serializers.CharField()
    away = serializers.CharField()
    match_result = serializers.CharField()
    sport_name = serializers.CharField()


class PlaceBetsSerializer(serializers.Serializer):
    selection = serializers.CharField()
    side = serializers.CharField()
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
