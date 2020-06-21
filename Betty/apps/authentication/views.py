from django.contrib.auth import login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from .serializers import CreateUserSerializer, LoginSerializer
from ..accounts.serializers import UserSerializer


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(
        responses={
            201: '',
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class LoginAPI(KnoxLoginView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: '',
            400: 'Bad Request'
        }
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginAPI, self).post(request, format=format)


class LogoutAPI(KnoxLogoutView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        responses={
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_204_NO_CONTENT: 'No Content'
        },
        manual_parameters=[
            openapi.Parameter('Authorization',
                              openapi.IN_HEADER,
                              description="Token <hash>",
                              type=openapi.TYPE_STRING)
        ]
    )
    def post(self, request, format=None):
        return super(LogoutAPI, self).post(request, format=format)
