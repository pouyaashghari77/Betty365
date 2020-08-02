from django.contrib import admin
from import_export.admin import ImportMixin
from import_export.resources import ModelResource

from Betty.apps.finance.models import WithdrawalRequest, Deposit


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created', 'updated']


class DepositResource(ModelResource):
    class Meta:
        model = Deposit
        import_id_fields = []
        fields = ('serial_num', 'code', 'amount', 'currency')

    def validate_instance(self, instance, import_validation_errors=None, validate_unique=True):
        instance.full_clean()
        return super(DepositResource, self).validate_instance(instance, import_validation_errors, validate_unique)


@admin.register(Deposit)
class DepositAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = DepositResource
    fields = ('user', 'payment_type', 'serial_num', 'code', 'amount',
              'currency', 'transaction_id', 'created', 'updated')
    list_display = ['serial_num', 'payment_type', 'code', 'transaction_id',
                    'amount', 'currency', 'created', 'updated', 'is_used']
    readonly_fields = ('created', 'updated')
