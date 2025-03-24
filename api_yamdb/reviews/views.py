from django.views.generic.edit import CreateView
from .models import Title, Category, Comment, Review, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from pprint import pprint


import requests

from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import GenreForm, TitleForm, ReviewForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)


class ContactsView(View):
    template_name = 'reviews/contacts.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class FaqView(View):
    template_name = 'reviews/FAQ.html'

    def get(self, request):
        return render(request, self.template_name)


title_context = {
    # 'create_url': 'reviews:create_title',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания

    'update_url': 'reviews:update_title',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования
    # 'cancel_url': 'reviews:title_detail',  # Для страницы редактирования

    'action': 'Добавить произведение',  # Для страницы списка
    'detail_url': 'reviews:title_detail',  # Для страницы списка

    'update_url': 'reviews:update_title',
    'delete_url': 'reviews:delete_title',
    'related_object_title': 'Отзывы',
    'no_related_objects_title': 'Отзывов нет',
    'create_related_object_title': 'Оставить отзыв',
}


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class TitleCreateView(CreateView):
    model = Title
    template_name = 'reviews/create_instance.html'
    form_class = TitleForm


    def get_success_url(self):
        return reverse_lazy(
            'reviews:titles'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = 'Добавить новое произведение'
        context['is_edit'] = False
        context["create_url"] = reverse("reviews:create_title")
        pprint(context)
        return context


class TitleUpdateView(UpdateView):
    model = Title
    form_class = TitleForm
    template_name = 'reviews/create_instance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = f'Изменить произведение {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('reviews:title_detail',  kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:title_detail', kwargs={'pk': self.kwargs['pk']}
        )


class TitleListView(ListView):
    model = Title
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = 'Список произведений'
        return context


# @method_decorator(login_required, name='dispatch')
class TitleDetailView(DetailView):
    model = Title
    template_name = 'reviews/instance_detail.html'
    # template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = f'Произведение {context["object"]}'
        context['related_object_list'] = Review.objects.filter(title_id=self.kwargs['pk'])
        context["update_url"] = reverse_lazy("reviews:update_title", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_title", kwargs={"pk": self.object.pk})
        context['create_related_object_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:titles')
        pprint(context)
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
        context.update(title_context)
        context['message'] = f'произведение {context["object"]}'
        context['cancel_url'] = reverse_lazy('reviews:title_detail',  kwargs={"pk": self.object.pk})
        pprint(context)
        return context


genre_context = {
    # 'create_url': 'reviews:create_genre',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания

    'update_url': 'reviews:update_genre',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования
    'cancel_url': 'reviews:genre_detail',  # Для страницы редактирования

    'action': 'Добавить жанр',  # Для страницы списка
    'detail_url': 'reviews:genre_detail',  # Для страницы списка

    'back_url': 'reviews:genres',  # Для страницы деталей
    'update_url': 'reviews:update_genre',
    'delete_url': 'reviews:delete_genre',
}

@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class GenreCreateView(CreateView):
    model = Genre
    template_name = 'reviews/create_instance.html'
    form_class = GenreForm


    def get_success_url(self):
        return reverse_lazy(
            'reviews:genres'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = 'Добавить новый жанр'
        context['is_edit'] = False
        return context


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'reviews/create_instance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Изменить жанр {context["object"]}'
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genres'
        )


class GenreListView(ListView):
    model = Genre
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = 'Список жанров'
        return context


# @method_decorator(login_required, name='dispatch')
class GenreDetailView(DetailView):
    model = Genre
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Жанр {context["object"]}'
        return context


class GenreDeleteView(DeleteView):
    model = Genre
    success_url = reverse_lazy("reviews:titles")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genres'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['message'] = f'Удалить жанр {context["object"]}'
        return context


review_context = {
    # 'create_url': 'reviews:create_review',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания
    'url_with_arg': True,

    'update_url': 'reviews:update_review',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования

    'action': 'Добавить отзыв',  # Для страницы списка
    'detail_url': 'reviews:review_detail',  # Для страницы списка

    'update_url': 'reviews:update_review',
    'delete_url': 'reviews:delete_review',
}

# @method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class ReviewCreateView(CreateView):
    model = Review
    template_name = 'reviews/create_instance.html'
    form_class = ReviewForm


    def get_success_url(self):
        title_id = self.kwargs['title_id']
        return reverse_lazy(
            'reviews:reviews', kwargs={'title_id': title_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = 'Добавить новый отзыв'
        context['is_edit'] = False
        title_id = self.kwargs['title_id']
        context['title_id'] = title_id
        context['create_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": title_id})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        title = Title.objects.get(pk=self.kwargs['title_id'])
        form.instance.title = title
        return super().form_valid(form)


class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_instance.html'
    # template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Изменить отзыв {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('reviews:review_detail',  kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        pprint(context)
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:review_detail',  kwargs={"title_id": self.object.title.pk, "pk": self.object.pk}
        )


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        title_id = self.kwargs['title_id']
        context['title'] = f'Список отзывов на произведение {Title.objects.get(pk=title_id)}'
        context['back_url'] = reverse_lazy('reviews:title_detail',  kwargs={"pk": title_id})
        context['create_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": title_id})
        pprint(context)
        return context

    def get_queryset(self):
        self.title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return Review.objects.filter(title=self.title)


# @method_decorator(login_required, name='dispatch')
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Отзыв {context["object"]}'
        context["update_url"] = reverse_lazy("reviews:update_review", kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_review", kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:reviews',  kwargs={"title_id": self.object.title.pk})
        pprint(context)
        return context


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy("reviews:reviews")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:reviews',  kwargs={"title_id": self.object.title.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['message'] = f'Удалить отзыв {context["object"]}'
        context['cancel_url'] = reverse_lazy('reviews:review_detail',  kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        return context



# from django.views.generic import CreateView
# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from .models import Review, Title
# from .forms import ReviewForm

# class ReviewCreateView(CreateView):
#     model = Review
#     form_class = ReviewForm
#     template_name = "reviews/review_form.html"

#     def dispatch(self, request, *args, **kwargs):
#         self.title = get_object_or_404(Title, id=self.kwargs["title_id"])
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.title = self.title
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("reviews:review_list", kwargs={"title_id": self.title.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = self.title
#         return context


# from django.views.generic import ListView
# from django.shortcuts import get_object_or_404
# from .models import Review, Title

# class ReviewListView(ListView):
#     model = Review
#     template_name = "reviews/instances.html"
#     # context_object_name = "reviews"

#     def get_queryset(self):
#         self.title = get_object_or_404(Title, id=self.kwargs["title_id"])
#         return Review.objects.filter(title=self.title)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = self.title
#         return context
