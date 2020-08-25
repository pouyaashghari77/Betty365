import requests
from django.utils.text import slugify
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Betty.apps.bets.models import Bet, Event
from Betty.apps.bets.serializers import (
    EventsRequestSerializer,
    UserBetsSerializer,
    PlaceBetsSerializer,
    EventsResultListSerializer
)
from Betty.apps.events.bwin import BWin


class EventsListAPI(APIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer(),
        responses={
            200: EventsResultListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        self.get_bwin_updates()

        qs = Event.objects.filter(
            match_result=Event.RESULT_UPCOMING,
        )
        if request.GET.get('sport_name'):
            qs = qs.filter(sport_name=request.GET.get('sport_name'))

        events = EventsResultListSerializer(qs, many=True).data

        return Response(data=events)

    def get_bwin_updates(self):
        bwin = BWin()
        result = bwin.preMatchResults()
        for element in result:
            if not element['HomeTeam']:
                continue
            event_title = '%s - %s' % (element['HomeTeam'], element['AwayTeam'])
            obj, _ = Event.objects.update_or_create(
                title=event_title,
                slug=slugify(event_title),
                defaults={
                    'title': event_title,
                    'slug': slugify(event_title),
                    'sport_name': element['SportName'],
                    'home': element['HomeTeam'],
                    'away': element['AwayTeam'],
                    'market_results': element['Markets'][0]['results'] if element['Markets'] else '',
                    'league': element['LeagueName'],
                    'region': element['RegionName'],
                    'date': element['Date'],
                    'external_id': element['Id'],
                },
            )


class LiveEventsListAPI(APIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer(),
        responses={
            200: EventsResultListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        self.get_bwin_updates()

        qs = Event.objects.filter(
            match_result=Event.RESULT_LIVE,
        )
        if request.GET.get('sport_name'):
            qs = qs.filter(sport_name=request.GET.get('sport_name'))

        events = EventsResultListSerializer(qs, many=True).data

        return Response(data=events)

    def get_bwin_updates(self):
        bwin = BWin()
        result = bwin.inplayResults()
        for element in result:
            if not element['HomeTeam']:
                continue
            event_title = '%s - %s' % (element['HomeTeam'], element['AwayTeam'])
            obj, _ = Event.objects.update_or_create(
                title=event_title,
                slug=slugify(event_title),
                defaults={
                    'title': event_title,
                    'slug': slugify(event_title),
                    'sport_name': element['SportName'],
                    'home': element['HomeTeam'],
                    'away': element['AwayTeam'],
                    'league': element['LeagueName'],
                    'region': element['RegionName'],
                    'date': element['Date'],
                    'external_id': element['Id'],
                    'match_result': Event.RESULT_LIVE
                },
            )


class UserBetsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserBetsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserBetsSerializer(many=True),
            401: 'Unauthorized'
        }
    )
    def get(self, request, *args, **kwargs):
        return super(UserBetsListAPIView, self).get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        bets = Bet.objects.filter(user=request.user)
        data = self.serializer_class(bets, many=True).data
        return Response(data)


class EventBetsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        request_body=PlaceBetsSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserBetsSerializer(many=True),
            401: 'Unauthorized'
        }
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        event = Event.objects.filter(slug=1).first()
        if event is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceBetsSerializer(
            data=request.data,
            context={'event': event, 'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        bet = serializer.create(serializer.validated_data)
        data = UserBetsSerializer(bet).data
        return Response(status=status.HTTP_201_CREATED, data=data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserBetsSerializer(many=True),
            401: 'Unauthorized'
        }
    )
    def get(self, request, *args, **kwargs):
        event = Event.objects.filter(slug=1).first()
        if event is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bets = Bet.objects.filter(event=event)
        data = UserBetsSerializer(bets, many=True).data
        return Response(data)


class ModifyBetAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        return

    def delete(self, request, *args, **kwargs):
        return
