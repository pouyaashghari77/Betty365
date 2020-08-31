from rest_framework import serializers

from Betty.apps.bets.models import Event


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
