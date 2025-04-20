import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import (Category, Comment, Genre, Review,
                            Title)
from users.models import ConfirmationCode, User

from .filters import TitleFilter
# from .models import ConfirmationCode
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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, created = User.objects.get_or_create(
            email=email, username=username)
        code = secrets.token_hex(16)

        ConfirmationCode.objects.update_or_create(
            user=user,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timedelta(hours=24)}
        )

        try:
            send_mail(
                subject='Код подтверждения для YaMDb',
                message=f'Ваш код подтверждения: {code}',
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
    serializer_class = ConfirmationCodeTokenSerializer

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


class MeView(APIView):

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.action == 'list':  # Разрешаем только список категорий
            return (ReadOnly(),)
        return (ReadOrAdminOnly(),)

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод не разрешен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод не разрешен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (ReadOrAdminOnly,)


class TitleViewSet(ModelViewSet):
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


class ReviewViewSet(ModelViewSet):

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
        serializer.save(author=user, title=title)


class CommentViewSet(ModelViewSet):

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
        serializer.save(
            author=user,
            review=review
        )

    def get_serializer_class(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return GetCommentSerializer
        return CommentWriteSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return (AuthorOrReadOnly(),)


class UserViewSet(ModelViewSet):
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
