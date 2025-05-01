import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from demo_auth.mixins import DemoAccessMixin
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ConfirmationCode, User

from .filters import TitleFilter
from .permissions import AdminOnly, AuthorOrReadOnly, ReadOnly, ReadOrAdminOnly
from .serializers import (CategorySerializer, CommentWriteSerializer,
                          ConfirmationCodeTokenSerializer, GenreSerializer,
                          GetCommentSerializer, GetReviewSerializer,
                          GetTitleSerializer, ReviewWriteSerializer,
                          SignUpSerializer, TitleWriteSerializer,
                          UserAdminSerializer, UserDetailSerializer,
                          UserUpdateSerializer)

logger = logging.getLogger(__name__)


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=SignUpSerializer,
        operation_id="Регистрация нового пользователя",
        operation_description=(
            "Получить код подтверждения на переданный email. "
            "Права доступа: Доступно без токена. "
            "Использовать имя 'me' в качестве username запрещено. "
            "Поля email и username должны быть уникальными."),
        responses={200: openapi.Response('OK', SignUpSerializer)}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, _ = User.objects.get_or_create(
            email=email, username=username)
        code = secrets.token_hex(16)
        token_url = request.build_absolute_uri(
            reverse('api:confirm_token')
        )

        # Проверяем, является ли пользователь демо
        is_demo = getattr(user, 'is_demo', False)

        ConfirmationCode.objects.update_or_create(
            user=user,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timedelta(hours=24),
                'is_demo': is_demo}
        )

        try:
            pass
            send_mail(
                subject='Код подтверждения для YaMDb',
                message=(
                    f'Ваш код подтверждения: {code}\n\n'
                    'Чтобы получить токен, отправьте запрос\n\n'
                    '{\n'
                    f'  "username": "{username}",\n'
                    f'  "confirmation_code": "{code}"\n'
                    '}\n\n'
                    f'на эндпоинт {token_url}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:  # Ловим только ошибки отправки email
            logger.error(f'Ошибка отправки email: {str(e)}')
            return Response(
                {
                    'status': 'error',
                    'email': email,
                    'detail': 'Не удалось отправить код'
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                'email': email,
                'username': username,
            },
            status=status.HTTP_200_OK
        )


class ConfirmationCodeTokenView(TokenObtainPairView):
    """Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена."""
    serializer_class = ConfirmationCodeTokenSerializer

    @swagger_auto_schema(
        operation_id="Получение JWT-токена",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            # Получаем код ошибки из сериализатора
            error_code = getattr(serializer, 'error_code', None)

            if error_code == 'not_found':
                return Response(
                    {'detail': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_id='Обновление JWT-токена',
        operation_description=(
            'Получение нового access-токена по действующему refresh-токену. '
            'Права доступа: Требуется валидный refresh-токен.'),
    )
    def post(self, request, *args, **kwargs):
        # Оставляем оригинальную логику, но теперь с правильной документацией
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            200: "Токен валиден (пустой ответ)",
            400: "Неверный формат токена или токен недействителен"
        },
        operation_id='Проверка валидности токена',
        operation_description=(
            "Проверка валидности токена. "
            "Возвращает 200 OK если токен действителен."),
    )
    def post(self, request, *args, **kwargs):
        # Оставляем оригинальную логику, но теперь с правильной документацией
        return super().post(request, *args, **kwargs)


class MeView(DemoAccessMixin, APIView):

    @swagger_auto_schema(
        operation_id="Получить данные текущего пользователя",
        responses={200: UserDetailSerializer}
    )
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Частичное обновление данных пользователя",
        request_body=UserUpdateSerializer,
        operation_id="me_update",
        responses={
            200: UserDetailSerializer,
            400: "Невалидные данные"
        }
    )
    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(
    DemoAccessMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (ReadOrAdminOnly,)


class GenreViewSet(DemoAccessMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (ReadOrAdminOnly,)


class TitleViewSet(DemoAccessMixin, ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (ReadOrAdminOnly(),)

    def get_serializer_class(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return GetTitleSerializer
        return TitleWriteSerializer


class ReviewViewSet(DemoAccessMixin, ModelViewSet):

    @property
    def title_id(self):
        return self.kwargs['title_id']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(title_id=self.title_id)

    def get_serializer_class(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return GetReviewSerializer
        return ReviewWriteSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (AuthorOrReadOnly(),)

    def perform_create(self, serializer):
        user = self.request.user
        title = get_object_or_404(Title, id=self.title_id)

        if Review.objects.filter(title_id=self.title_id, author=user).exists():
            raise ValidationError(
                {'detail': 'Вы уже оставляли отзыв на это произведение.'}
            )
        instance = serializer.save(author=user, title=title)
        self._maybe_set_demo(instance)


class CommentViewSet(DemoAccessMixin, ModelViewSet):

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.filter(review_id=self.review_id).order_by('id')

    def perform_create(self, serializer):
        user = self.request.user
        review = get_object_or_404(Review, id=self.review_id)
        instance = serializer.save(
            author=user,
            review=review
        )
        self._maybe_set_demo(instance)

    def get_serializer_class(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return GetCommentSerializer
        return CommentWriteSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (AuthorOrReadOnly(),)


class UserViewSet(DemoAccessMixin, ModelViewSet):
    model = get_user_model()
    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return UserDetailSerializer
        return UserAdminSerializer

    def get_permissions(self):
        return (AdminOnly(),)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
