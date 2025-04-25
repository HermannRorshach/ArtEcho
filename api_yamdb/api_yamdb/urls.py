from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_office.urls')),
    path('', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('reviews.urls')),
    path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
