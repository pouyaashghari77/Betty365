from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from Betty.apps.bets.models import Event
from Betty.apps.events.serializers import EventsRequestSerializer, EventsResultListSerializer


class EventsListAPI(APIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer(),
        responses={
            200: EventsResultListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        qs = Event.objects.filter(
            match_result=Event.RESULT_UPCOMING,
        )
        if request.GET.get('sport_name'):
            qs = qs.filter(sport_name=request.GET.get('sport_name'))

        events = EventsResultListSerializer(qs, many=True).data

        return Response(data=events)


class LiveEventsListAPI(APIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer(),
        responses={
            200: EventsResultListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        qs = Event.objects.filter(
            match_result=Event.RESULT_LIVE,
        )
        if request.GET.get('sport_name'):
            qs = qs.filter(sport_name=request.GET.get('sport_name'))

        events = EventsResultListSerializer(qs, many=True).data

        return Response(data=events)
