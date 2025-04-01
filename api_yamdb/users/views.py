from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import CreationForm


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')


class CustomLoginView(LoginView):
    success_url = reverse_lazy('reviews:titles')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('reviews:titles')
        return super().dispatch(request, *args, **kwargs)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('reviews:titles')
    template_name = 'users/signup.html'


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        # Надо создать маршрут для создания пользователя
        context["create_url"] = reverse_lazy("reviews:create_title")
        context['display_fields'] = [
            "first_name", "last_name", "username", "date_joined", "role", "bio",
            "last_login"]
        context['action'] = 'Добавить пользователя'
        # pprint(context)
        return context