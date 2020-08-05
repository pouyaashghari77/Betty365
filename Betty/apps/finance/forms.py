from django import forms

from Betty.apps.finance.models import WithdrawalRequest


class WithdrawalRequestForm(forms.ModelForm):
    def save(self, commit=True):
        approve = self.cleaned_data.get('status') == WithdrawalRequest.STATUS_APPROVED
        is_pending = self.initial.get('status') == WithdrawalRequest.STATUS_PENDING
        if approve and is_pending:
            self.instance.user.decrease_balance(self.instance.amount)
        return super(WithdrawalRequestForm, self).save(commit=commit)
