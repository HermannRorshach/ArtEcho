from decouple import config
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .authorized_user_func import restore_user_data

NALIVKIN_USERNAME = config('NALIVKIN_USERNAME')
NALIVKIN_PASSWORD = config('NALIVKIN_PASSWORD')


class AuthorizedUserLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        restore_user_data()
        user = authenticate(
            request,
            username=NALIVKIN_USERNAME,
            password=NALIVKIN_PASSWORD
        )
        if user is not None:
            login(request, user)
            return redirect('posts:index')
        return redirect('users:login')
