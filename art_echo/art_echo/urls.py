from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_office.urls')),
    path('', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('reviews.urls')),
    path('', include('api.urls')),
    path('', include('demo_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
