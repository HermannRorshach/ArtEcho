from decouple import config
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View

from .restore_data_for_demo import reset_demo_data

NALIVKIN_USERNAME = config('NALIVKIN_USERNAME')
NALIVKIN_PASSWORD = config('NALIVKIN_PASSWORD')


class DemoWelcomeView(View):
    template_name = 'demo_auth/demo_welcome.html'

    def get(self, request):
        return render(request, self.template_name)


class DemoUserLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        reset_demo_data()
        user = authenticate(
            request,
            username=NALIVKIN_USERNAME,
            password=NALIVKIN_PASSWORD
        )
        if user is not None:
            login(request, user)
            return redirect('reviews:titles')
        return redirect('users:login')
