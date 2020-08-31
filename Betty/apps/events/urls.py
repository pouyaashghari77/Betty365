from django.urls import path

from Betty.apps.events.views import EventsListAPI, LiveEventsListAPI

urlpatterns = [
    path("events/", EventsListAPI.as_view()),
    path("events/live/", LiveEventsListAPI.as_view()),
]
