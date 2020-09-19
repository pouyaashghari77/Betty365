from django.urls import path

from Betty.apps.bets.views import (
    UserBetsListAPIView,
    EventBetsAPIView, ModifyBetAPIView
)

urlpatterns = [
    path("events/<slug:event_slug>/bets/", EventBetsAPIView.as_view()),
    path("users/self/bets/", UserBetsListAPIView.as_view()),
    path("users/self/bets/<int:bet_id>/", ModifyBetAPIView.as_view())
]
