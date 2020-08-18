from django import forms

from Betty.apps.finance.models import WithdrawalRequest


class WithdrawalRequestForm(forms.ModelForm):
    def save(self, commit=True):
        cancel = self.cleaned_data.get('status') == WithdrawalRequest.STATUS_CANCELLED
        is_approved = self.initial.get('status') == WithdrawalRequest.STATUS_APPROVED
        if cancel and is_approved:
            self.instance.user.increase_balance(self.instance.amount)
        return super(WithdrawalRequestForm, self).save(commit=commit)
