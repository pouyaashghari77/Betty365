from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Betty.apps.bets.models import Event
from Betty.apps.events.serializers import EventsRequestSerializer, EventsResultListSerializer


class EventsListAPI(ListAPIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer(),
        responses={
            200: EventsResultListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_qs(request)
        events = EventsResultListSerializer(qs, many=True).data
        now = timezone.localtime(timezone.now())
        return Response(data=events, headers={'x-server-time': now})

    def get_qs(self, request):
        live = request.GET.get('live') == 'true'
        qs = Event.objects.filter(
            match_result=Event.RESULT_LIVE if live else Event.RESULT_UPCOMING,
        )
        sport_name = request.GET.get('sport_name')
        league = request.GET.get('league')
        if sport_name:
            qs = qs.filter(sport_name__iexact=sport_name)
        if league:
            qs = qs.filter(league__icontains=league)
        return qs
