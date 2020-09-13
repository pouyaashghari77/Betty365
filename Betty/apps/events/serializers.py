from rest_framework import serializers

from Betty.apps.bets.models import Event


class EventsRequestSerializer(serializers.Serializer):
    sport_name = serializers.CharField(required=False, default='')
    league = serializers.CharField(required=False, default='')
    live = serializers.BooleanField(required=False, default=False)


class EventsResultListSerializer(serializers.ModelSerializer):
    period = serializers.ReadOnlyField(required=False, default='')
    live_score = serializers.ReadOnlyField(required=False, default='')

    class Meta:
        model = Event
        exclude = ['external_id', 'scoreboard']


class ShortEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    home = serializers.CharField()
    away = serializers.CharField()
    match_result = serializers.CharField()
    sport_name = serializers.CharField()
