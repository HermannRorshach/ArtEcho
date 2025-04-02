from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from reviews.utils import IsAdminOrSuperuser

from .forms import CreationForm

User = get_user_model()

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


user_context = {
    'create_button_text': 'Добавить пользователя',

    'update_url': 'users:update_user',
    'update_button_text': 'Изменить',

    'action': 'Добавить пользователя',
    'detail_url': 'users:user_detail',

    'update_url': 'users:update_user',
    'delete_url': 'users:delete_user',
}



class UserCreateView(IsAdminOrSuperuser, CreateView):
    model = User
    template_name = 'reviews/create_instance.html'
    form_class = CreationForm


    def get_success_url(self):
        return reverse_lazy(
            'users:users'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = 'Добавить нового пользователя'
        context['is_edit'] = False
        context["create_url"] = reverse_lazy("users:create_user")
        return context


class UserUpdateView(IsAdminOrSuperuser, UpdateView):
    model = User
    form_class = CreationForm
    template_name = 'reviews/create_instance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = f'Изменить пользователя {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('users:user_detail',  kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'users:user_detail', kwargs={'pk': self.kwargs['pk']}
        )



class UserDetailView(DetailView):
    model = User
    template_name = 'reviews/instance_detail.html'
    # template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = f'Произведение {context["object"]}'
        context["update_url"] = reverse_lazy("users:update_user", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("users:delete_user", kwargs={"pk": self.object.pk})
        context['back_url'] = reverse_lazy('users:users')
        context['display_fields'] = [
            "first_name", "last_name", "username", "date_joined", "role", "bio",
            "last_login"]

        return context


class UserDeleteView(IsAdminOrSuperuser, DeleteView):
    model = User
    success_url = reverse_lazy("users:users")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'users:users'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['message'] = f'Пользователь {context["object"]}'
        context['cancel_url'] = reverse_lazy('users:user_detail',  kwargs={"pk": self.object.pk})
        return context

class UsersListView(IsAdminOrSuperuser, ListView):
    model = User
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = 'Список пользователей'
        # Надо создать маршрут для создания пользователя
        context["create_url"] = reverse_lazy("users:create_user")
        context['display_fields'] = [
            "first_name", "last_name", "username", "date_joined", "role", "bio",
            "last_login"]
        return context