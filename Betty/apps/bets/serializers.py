from rest_framework import serializers

from Betty.apps.bets.models import Bet, Deposit, WithdrawalRequest


class EventsRequestSerializer(serializers.Serializer):
    sport = serializers.CharField(required=False, default='')
    country = serializers.CharField(required=False, default='')
    league = serializers.CharField(required=False, default='')


class EventSerializer(serializers.Serializer):
    title = serializers.CharField()
    home = serializers.CharField()
    away = serializers.CharField()
    result = serializers.CharField()


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
    event = EventSerializer()
    selection = serializers.CharField()
    side = serializers.CharField()
    odds = serializers.FloatField()
    stake = serializers.FloatField()
    matched = serializers.BooleanField()
    has_won = serializers.NullBooleanField()


class DepositSerializer(serializers.ModelSerializer):
    serial_num = serializers.CharField()
    code = serializers.CharField()
    amount = serializers.FloatField()
    created = serializers.DateTimeField(allow_null=True)
    updated = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Deposit
        fields = ['serial_num', 'code', 'amount', 'created', 'updated']


class RequestWithdrawalSerializer(serializers.Serializer):
    amount = serializers.FloatField()


class UserWithdrawalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'created', 'updated']
