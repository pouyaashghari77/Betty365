from django.urls import path

from Betty.apps.accounts.views import UserInfoAPIView

urlpatterns = [
    path('users/self/info/', UserInfoAPIView.as_view(), name='user-info'),
]
