from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Betty.apps.finance.models import Deposit, WithdrawalRequest


class MakePrepaidCardDepositSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate_code(self, code):
        qs = Deposit.objects.filter(code=code)
        if not qs.exists():
            raise ValidationError('Deposit with this code does not exist.')
        if not qs.filter(is_used=False).exists():
            raise ValidationError('This code has been used.')
        return code


class MakePrepaidCardDepositResponseSerializer(serializers.Serializer):
    balance = serializers.FloatField()


class DepositSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(allow_null=True)
    updated = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Deposit
        fields = ['payment_type', 'serial_num', 'code', 'amount', 'transaction_id',
                  'currency', 'is_used', 'created', 'updated']


class RequestWithdrawalSerializer(serializers.Serializer):
    amount = serializers.FloatField()


class UserWithdrawalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'created', 'updated']
