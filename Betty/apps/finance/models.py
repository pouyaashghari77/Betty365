from django.core.exceptions import ValidationError
from django.db import models

from Betty.apps.constants import CURRENCY_CHOICES, CURRENCY_EURO


class WithdrawalRequest(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_REJECTED, 'Rejected'),
    )
    amount = models.FloatField('Amount', default=0, null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='withdrawal_requests',
                             verbose_name='User')
    status = models.CharField('Status', choices=STATUS_CHOICES, default=STATUS_PENDING,
                              max_length=32, blank=True, null=True)
    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Withdrawal Request'
        verbose_name_plural = 'Withdrawal Requests'

    def __str__(self):
        return f'{self.user} - amount:{self.amount} - {self.status}'


class Deposit(models.Model):
    PAYMENT_TYPE_PREPAID = 'Prepaid Card'
    PAYMENT_TYPE_DEBIT_CARD = 'Debit Card'
    PAYMENT_TYPE_BANK_TRANSFER = 'Bank Transfer'
    PAYMENT_TYPE_CASH = 'Cash'
    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_PREPAID, PAYMENT_TYPE_PREPAID),
        (PAYMENT_TYPE_DEBIT_CARD, PAYMENT_TYPE_DEBIT_CARD),
        (PAYMENT_TYPE_BANK_TRANSFER, PAYMENT_TYPE_BANK_TRANSFER),
        (PAYMENT_TYPE_CASH, PAYMENT_TYPE_CASH)
    )
    payment_type = models.CharField('Payment Type', max_length=16,
                                    choices=PAYMENT_TYPE_CHOICES,
                                    default=PAYMENT_TYPE_PREPAID)
    serial_num = models.BigIntegerField('Serial Number', unique=True)
    code = models.BigIntegerField('Code', unique=True,
                                  blank=True, null=True)
    amount = models.FloatField('Amount', default=0)
    currency = models.CharField('Currency', max_length=16,
                                choices=CURRENCY_CHOICES,
                                default=CURRENCY_EURO)
    transaction_id = models.CharField('Transaction ID', max_length=64,
                                      blank=True, null=True)
    is_used = models.NullBooleanField('Is Used', default=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             related_name='deposits',
                             null=True, blank=True,
                             verbose_name='User')

    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'

    def __str__(self):
        return str(self.code)

    def clean(self):
        if self.is_prepaid_card and len(str(self.code)) != 16:
            raise ValidationError('Make sure that the code is exactly 16 digits.')

    def is_prepaid_card(self):
        return self.payment_type == self.PAYMENT_TYPE_PREPAID

    def use_prepaid_card_code(self, user):
        if self.is_used:
            return

        user.increase_balance(self.amount)
        self.is_used = True
        self.user = user
        self.save()
