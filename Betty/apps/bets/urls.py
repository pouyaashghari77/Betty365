from django.urls import path

from Betty.apps.bets.views import (
    EventsListAPI, UserBetsListAPIView,
    EventBetsAPIView, ModifyBetAPIView,
    UserDepositsList, DepositDetail
)

urlpatterns = [
    path("events/", EventsListAPI.as_view()),
    path("events/<slug:slug>/bets/", EventBetsAPIView.as_view()),
    path("events/<slug:slug>/bets/<int:id>/", ModifyBetAPIView.as_view()),

    path("users/self/bets/", UserBetsListAPIView.as_view()),
    path("users/self/deposits/", UserDepositsList.as_view()),
    path("users/self/deposits/<str:serial_num>/", DepositDetail.as_view())
]
