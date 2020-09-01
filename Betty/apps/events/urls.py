from django.urls import path

from Betty.apps.events.views import EventsListAPI

urlpatterns = [
    path("events/", EventsListAPI.as_view())
]
