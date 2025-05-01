from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from demo_auth.mixins import DemoAccessMixin
from reviews.models import Comment, Review
from reviews.utils import IsAdminOrSuperuser, IsStaffMixin
from reviews.views import CommentListView, ReviewListView
from users.views import UserDeleteView, UserDetailView, UserUpdateMixin

from .forms import AdminCreationForm, AdminUpdateForm

User = get_user_model()


class CabinetView(IsStaffMixin, View):
    template_name = 'admin_office/cabinet.html'

    def get(self, request, *args, **kwargs):
        links = [
            {
                'url': reverse('reviews:genres'),
                'text': 'Жанры',
                'check': IsStaffMixin.check_permission,
            },
            {
                'url': reverse('reviews:categories'),
                'text': 'Категории',
                'check': IsStaffMixin.check_permission,
            },
            {
                'url': reverse('reviews:titles'),
                'text': 'Произведения',
                'check': IsStaffMixin.check_permission,
            },
            {
                'url': reverse('admin_office:cabinet_reviews'),
                'text': 'Все отзывы',
                'check': IsStaffMixin.check_permission,
            },
            {
                'url': reverse('admin_office:cabinet_comments'),
                'text': 'Все комментарии',
                'check': IsStaffMixin.check_permission,
            },
            {
                'url': reverse('admin_office:users'),
                'text': 'Список пользователей',
                'check': IsAdminOrSuperuser.check_permission,
            },
        ]

        visible_links = [
            {'url': link['url'], 'text': link['text']}
            for link in links if link['check'](request.user)
        ]

        return render(
            request, self.template_name, {'links': visible_links})


class CabinetReviewsListView(IsStaffMixin, ReviewListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список отзывов'
        context['back_url'] = reverse_lazy('admin_office:cabinet')
        del context['create_url']
        return context

    def get_queryset(self):
        queryset = Review.objects.all().order_by('-pk')
        return self.filter_queryset(queryset)


class CabinetCommentListView(IsStaffMixin, CommentListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все комментарии'
        context['back_url'] = reverse_lazy('admin_office:cabinet')
        del context['create_url']
        return context

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-pk')
        return self.filter_queryset(queryset)


class UserCreateView(IsAdminOrSuperuser, DemoAccessMixin, CreateView):
    model = User
    template_name = 'reviews/create_instance.html'
    form_class = AdminCreationForm

    def get_success_url(self):
        return reverse_lazy(
            'users:users'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить нового пользователя'
        context['create_button_text'] = 'Добавить пользователя'
        context['action'] = 'Добавить пользователя'
        context['is_edit'] = False
        context["create_url"] = reverse_lazy('admin_office:create_user')
        return context


class CabinetUserDetailView(IsAdminOrSuperuser, UserDetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('admin_office:users')
        context['display_fields'] = [
            'bio', 'role', 'avatar', 'birth_date', 'sex', 'city',
            'relationship_status', 'vk_url', 'youtube_url',
            'telegram_url', 'whatsapp_url', 'email', 'date_joined',
            'last_login'
        ]
        context['update_url'] = reverse_lazy(
            'admin_office:admin_update_user',
            kwargs={'username': self.object.username})
        context['delete_url'] = reverse_lazy(
            'admin_office:admin_delete_user',
            kwargs={'username': self.object.username})
        context['can_edit'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        context['can_delete'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        context['cancel_url'] = reverse_lazy(
            'users:admin_user_detail',
            kwargs={'username': self.object.username})
        return context


class CabinetUserUpdateView(IsAdminOrSuperuser, UserUpdateMixin):
    form_class = AdminUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изменить пользователя {context["object"]}'
        context['cancel_url'] = reverse_lazy(
            'admin_office:admin_user_detail',
            kwargs={'username': self.object.username})
        return context

    def dispatch(self, request, *args, **kwargs):
        if not IsAdminOrSuperuser.check_permission(self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'admin_office:admin_user_detail',
            kwargs={'username': self.object.username}
        )


class CabinetUserDeleteView(IsAdminOrSuperuser, UserDeleteView):

    def dispatch(self, request, *args, **kwargs):
        if not IsAdminOrSuperuser.check_permission(
            self.request.user
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy(
            'admin_office:admin_user_detail',
            kwargs={'username': self.object.username})
        print(context)
        return context
