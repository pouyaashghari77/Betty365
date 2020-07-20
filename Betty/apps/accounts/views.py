from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..accounts.serializers import UserSerializer


class UserInfoAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Bearer <access_token>",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserSerializer,
            401: 'Unauthorized'
        }
    )
    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)
