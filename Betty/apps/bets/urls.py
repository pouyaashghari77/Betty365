from django.urls import path

from Betty.apps.bets.views import (
    UserBetsListAPIView,
    EventBetsAPIView, ModifyBetAPIView
)

urlpatterns = [
    path("events/<slug:slug>/bets/", EventBetsAPIView.as_view()),
    path("events/<slug:slug>/bets/<int:id>/", ModifyBetAPIView.as_view()),
    path("users/self/bets/", UserBetsListAPIView.as_view()),
]
