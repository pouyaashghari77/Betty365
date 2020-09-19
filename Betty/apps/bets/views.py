from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Betty.apps.bets.models import Bet, Event
from Betty.apps.bets.serializers import (
    UserBetsSerializer,
    PlaceBetsSerializer
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
    def post(self, request, event_slug, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        event = Event.objects.filter(slug=event_slug).last()
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
    def get(self, request, event_slug, *args, **kwargs):
        event = Event.objects.filter(slug=event_slug).last()
        if event is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bets = Bet.objects.filter(event=event)
        data = UserBetsSerializer(bets, many=True).data
        return Response(data)


class ModifyBetAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        return
