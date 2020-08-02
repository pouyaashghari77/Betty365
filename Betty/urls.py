from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

...

schema_view = get_schema_view(
    openapi.Info(
        title="Betty365 APIs",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path("", include('Betty.apps.accounts.urls')),
    path("", include('Betty.apps.authentication.urls')),
    path("", include('Betty.apps.bets.urls')),
    path("", include('Betty.apps.finance.urls')),
]
