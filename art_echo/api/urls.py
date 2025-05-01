import os

from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
desc_path = os.path.join(BASE_DIR, 'docs', 'api_description.txt')

with open(desc_path, 'r', encoding='utf-8') as f:
    description = f.read()


schema_view = get_schema_view(
    openapi.Info(
        title="ArtEcho API",
        default_version='v1',
        description=description,
        contact=openapi.Contact(email="figasenedosuk@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_name = 'api'

router = DefaultRouter()
router.register(
    'categories',
    views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/auth/signup/', views.SignUpView.as_view(), name='sign_up'),
    path(
        'api/v1/auth/token/',
        views.ConfirmationCodeTokenView.as_view(), name='confirm_token'),
    path(
        'api/v1/auth/token/refresh/',
        views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path(
        'api/v1/auth/token/verify/',
        views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/users/me/', views.MeView.as_view(), name='me'),
    path('api/v1/', include(router.urls)),
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(
        r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
