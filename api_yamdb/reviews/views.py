from django.views.generic.edit import CreateView
from .models import Title, Category, Comment, Review, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required


import requests

from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import TitleForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class TitleCreateView(CreateView):
    model = Title
    template_name = 'reviews/create_title.html'
    form_class = TitleForm


    def get_success_url(self):
        return reverse_lazy(
            'reviews:titles'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новое произведение'
        context['is_edit'] = False
        context['create_url'] = 'reviews:create_title'
        context['create_button_text'] = 'Добавить'
        return context


class TitleUpdateView(UpdateView):
    model = Title
    form_class = TitleForm
    template_name = 'reviews/create_title.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изменить произведение {context["object"]}'
        context['is_edit'] = True
        context['update_url'] = 'reviews:update_title'
        context['update_button_text'] = 'Изменить'
        context['cancel_url'] = 'reviews:title_detail'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:titles'
        )


class TitleListView(ListView):
    model = Title
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список произведений'
        return context


# @method_decorator(login_required, name='dispatch')
class TitleDetailView(DetailView):
    model = Title
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Произведение {context["object"]}'
        return context


class TitleDeleteView(DeleteView):
    model = Title
    success_url = reverse_lazy("reviews:titles")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:titles'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить произведение {context["object"]}'
        return context
