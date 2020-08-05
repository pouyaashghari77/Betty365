from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Betty.apps.finance.models import Deposit, WithdrawalRequest
from Betty.apps.finance.serializers import (
    DepositSerializer,
    UserWithdrawalDetailSerializer,
    RequestWithdrawalSerializer, MakePrepaidCardDepositSerializer, MakePrepaidCardDepositResponseSerializer
)


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


class MakePrepaidCardDepositAPIView(APIView):
    @swagger_auto_schema(
        request_body=MakePrepaidCardDepositSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: MakePrepaidCardDepositResponseSerializer,
            401: 'Unauthorized'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = MakePrepaidCardDepositSerializer(data=request.data)
        if serializer.is_valid():
            deposit = Deposit.objects.get(code=serializer.validated_data['code'],
                                          payment_type=Deposit.PAYMENT_TYPE_PREPAID)
            deposit.use_prepaid_card_code(request.user)

            request.user.refresh_from_db()

            return Response(
                data={'balance': request.user.balance},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = RequestWithdrawalSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            withdrawal_req = serializer.save()
            return Response(UserWithdrawalDetailSerializer(withdrawal_req).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
