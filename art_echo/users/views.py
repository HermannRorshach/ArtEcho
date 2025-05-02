from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from demo_auth.mixins import DemoAccessMixin
from reviews.utils import IsAdminOrSuperuser, is_owner

from .forms import PublicCreationForm, PublicUpdateForm

User = get_user_model()


class CustomLogoutView(LogoutView):
    template_name = 'users/logged_out.html'

    @method_decorator(require_GET)
    def dispatch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


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
    form_class = PublicCreationForm
    success_url = reverse_lazy('reviews:titles')
    template_name = 'users/signup.html'


user_context = {
    'action': 'Добавить пользователя',

    'update_url': 'users:update_user',
    'update_button_text': 'Изменить',

    'detail_url': 'users:user_detail',

    'update_url': 'users:update_user',
    'delete_url': 'users:delete_user',

    'avatar': True,
}


class UserUpdateMixin(DemoAccessMixin, UpdateView):
    model = User
    form_class = PublicUpdateForm
    template_name = 'reviews/create_instance.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = 'Изменить анкету'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'users:user_detail', kwargs={'username': self.object.username})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'users:user_detail', kwargs={'username': self.object.username}
        )


class UserUpdateView(UserUpdateMixin):

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not is_owner(request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(DemoAccessMixin, DetailView):
    model = User
    template_name = 'reviews/instance_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = f'Произведение {context["object"]}'
        context['update_url'] = reverse_lazy(
            'users:update_user', kwargs={'username': self.object.username})
        context['delete_url'] = reverse_lazy(
            'users:delete_user', kwargs={'username': self.object.username})
        context['display_fields'] = [
            'bio', 'role', 'avatar', 'birth_date', 'sex', 'city',
            'relationship_status', 'vk_url', 'youtube_url',
            'telegram_url', 'whatsapp_url'
        ]
        context['can_edit'] = is_owner(
            self.request.user, context['object']
        )
        context['can_delete'] = is_owner(
            self.request.user, context['object']
        )

        return context


class UserDeleteView(DemoAccessMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:users')
    template_name = 'reviews/confirm_delete.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (
            is_owner(request.user, self.object)
            or IsAdminOrSuperuser.check_permission(request.user)
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if is_owner(self.request.user, self.object):
            return reverse_lazy('reviews:titles')
        return reverse_lazy('users:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['message'] = f'Пользователь {context["object"]}'
        context['cancel_url'] = reverse_lazy(
            'users:user_detail', kwargs={'username': self.object.username})
        return context


class UsersListView(IsAdminOrSuperuser, DemoAccessMixin, ListView):
    model = User
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_context)
        context['title'] = 'Список пользователей'
        context['create_url'] = reverse_lazy('admin_office:create_user')
        context['display_fields'] = [
            'first_name', 'last_name', 'username', 'date_joined', 'role',
            'bio', 'last_login']
        return context


class MeView(UserDetailView):
    def get_object(self, queryset=None):
        return self.request.user
