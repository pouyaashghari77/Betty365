from django.urls import path

from .views import UserDepositsList, WithdrawalRequestAPI, MakePrepaidCardDepositAPIView

urlpatterns = [
    path("prepaid-card-deposit/", MakePrepaidCardDepositAPIView.as_view()),
    path("deposits/", UserDepositsList.as_view()),
    path("withdrawals/", WithdrawalRequestAPI.as_view()),
]
