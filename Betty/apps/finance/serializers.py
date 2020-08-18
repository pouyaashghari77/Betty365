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

    def validate_amount(self, value):
        if value > self.context.get('user').balance:
            raise ValidationError('Withdrawal request amount can not be more than the balance.')
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        withdrawal_request = WithdrawalRequest.objects.create(
            status=WithdrawalRequest.STATUS_APPROVED,
            amount=validated_data['amount'],
            user=user
        )
        user.decrease_balance(validated_data['amount'])
        return withdrawal_request


class UserWithdrawalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'status', 'created', 'updated']

    def to_representation(self, instance):
        data = super(UserWithdrawalDetailSerializer, self).to_representation(instance)
        user = instance.user
        user.refresh_from_db()
        data['balance'] = user.balance
        return data
