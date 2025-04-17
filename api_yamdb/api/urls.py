from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

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
    path('v1/auth/signup/', views.SignUpView.as_view(), name='sign_up'),
    path(
        'v1/auth/token/',
        views.ConfirmationCodeTokenView.as_view(), name='confirm_token'),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'v1/auth/token/verify/',
        TokenVerifyView.as_view(), name='token_verify'),
    path('v1/users/me/', views.MeView.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
