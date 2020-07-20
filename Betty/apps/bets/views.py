import requests
from django.http import Http404
from django.utils.text import slugify
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Betty.apps.bets.models import Bet, Event, Deposit, WithdrawalRequest
from Betty.apps.bets.serializers import (
    EventsRequestSerializer,
    UserBetsSerializer,
    PlaceBetsSerializer,
    DepositSerializer,
    RequestWithdrawalSerializer, UserWithdrawalDetailSerializer
)


class EventsListAPI(APIView):
    @swagger_auto_schema(
        query_serializer=EventsRequestSerializer,
    )
    def get(self, request, *args, **kwargs):
        headers = {
            'apikey': '4d532b80-9eb1-11ea-bb05-f1dead435c5f',
        }
        params = EventsRequestSerializer(request.query_params).data

        resp = requests.get(
            'http://app.oddsapi.io/api/v1/odds',
            headers=headers,
            params=params
        ).json()

        for element in resp:
            sites = element.pop('sites', None)
            odds = list(sites['1x2'].values())[1]['odds']
            element['event']['odds'] = odds
            event_title = '%s - %s' % (element['event']['home'], element['event']['away'])
            obj, _ = Event.objects.update_or_create(
                title=event_title,
                slug=slugify(event_title),
                defaults={
                    'title': event_title,
                    'slug': slugify(event_title),
                    'home': element['event']['home'],
                    'away': element['event']['away'],
                    'home_odds': element['event']['odds']['1'],
                    'away_odds': element['event']['odds']['2'],
                    'draw_odds': element['event']['odds']['X'],
                    'date': element['event']['start_time'],
                },
            )

        return Response(data=resp)


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


class UserDepositsList(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: DepositSerializer(many=True),
            401: 'Unauthorized'
        }
    )
    def get(self, request, *args, **kwargs):
        deposits = Deposit.objects.filter(user=request.user)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositDetail(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, serial_num, *args, **kwargs):
        try:
            deposit = Deposit.objects.get(serial_num=serial_num, user=request.user)
        except Deposit.DoesNotExist:
            raise Http404

        if deposit.created is None:
            serializer = DepositSerializer(deposit)
            response_data = serializer.data
            deposit.save()
            return Response(response_data, status=status.HTTP_200_OK)

        deposit.code = '200 EURO'
        serializer = DepositSerializer(deposit)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, serial_num, *args, **kwargs):
        try:
            deposit = Deposit.objects.get(serial_num=serial_num)
        except Deposit.DoesNotExist:
            raise Http404

        serializer = DepositSerializer(deposit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serial_num, *args, **kwargs):
        try:
            deposit = Deposit.objects.get(serial_num=serial_num)
        except Deposit.DoesNotExist:
            raise Http404

        deposit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WithdrawalRequestAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserWithdrawalDetailSerializer(many=True),
            401: 'Unauthorized'
        }
    )
    def get(self, request, *args, **kwargs):
        withdrawal_reqs = WithdrawalRequest.objects.filter(user=request.user)
        serializer = UserWithdrawalDetailSerializer(withdrawal_reqs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=RequestWithdrawalSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            201: UserWithdrawalDetailSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RequestWithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            withdrawal_req = serializer.save()
            return Response(UserWithdrawalDetailSerializer(withdrawal_req).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
