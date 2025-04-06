from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView)
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
# Вызываем метод .register с нужными параметрами
# router.register('me', views.MeView, basename='me')

urlpatterns = [
    path('v1/auth/token/', views.ConfirmationCodeTokenView.as_view(), name='confirm_token'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='sign_up'),
    # path('', include(router.urls)),
    path('v1/users/me/', views.MeView.as_view(), name='me'),
]
