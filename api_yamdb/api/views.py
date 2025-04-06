import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from .models import ConfirmationCode
from .serializers import (ConfirmationCodeTokenSerializer, SignUpSerializer,
                          UserDetailSerializer, UserUpdateSerializer)

logger = logging.getLogger(__name__)


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, created = User.objects.get_or_create(email=email, username=username)
        code = secrets.token_hex(16)

        ConfirmationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': timezone.now() + timedelta(hours=24)}
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
            logger.error(f"Ошибка отправки email: {str(e)}")
            return Response(
                {'status': 'error', 'email': email, 'detail': 'Не удалось отправить код'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                'status': 'success',
                'email': email,
                'detail': 'Код отправлен',
                'user_exists': not created
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class ConfirmationCodeTokenView(TokenObtainPairView):
    serializer_class = ConfirmationCodeTokenSerializer



class MeView(APIView):
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)