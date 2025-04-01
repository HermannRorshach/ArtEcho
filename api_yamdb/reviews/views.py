from pprint import pprint

import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CategoryForm, CommentForm, GenreForm, ReviewForm, TitleForm
from .models import Category, Comment, Genre, Review, Title


def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)


class ContactsView(View):
    template_name = 'reviews/contacts.html'

    def get(self, request):
        return render(request, self.template_name)

class FigView(View):
    template_name = 'reviews/fig.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class FaqView(View):
    template_name = 'reviews/FAQ.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CabinetView(View):
    template_name = 'reviews/cabinet.html'

    def get(self, request, *args, **kwargs):
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
        context["create_url"] = reverse_lazy("reviews:create_title")
        pprint(context)
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
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
        context["create_url"] = reverse_lazy("reviews:create_title")
        context['genres_list'] = Genre.objects.all()
        context['category_list'] = Category.objects.all()
        context['display_fields'] = ["year", "category", "genre"]
        # pprint(context)
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
        context['create_related_object_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": self.object.pk})
        context["update_url"] = reverse_lazy("reviews:update_title", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_title", kwargs={"pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:titles')
        context['display_fields'] = ["year", "category", "genre"]
        pprint(context)
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
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
        context["create_url"] = reverse_lazy("reviews:create_genre")
        context['cancel_url'] = reverse_lazy('reviews:genres')
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'reviews/create_instance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Изменить жанр {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('reviews:genre_detail',  kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genre_detail', kwargs={'pk': self.kwargs['pk']}
        )


class GenreListView(ListView):
    model = Genre
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = 'Список жанров'
        context["create_url"] = reverse_lazy("reviews:create_genre")
        del context["back_url"]
        context['display_fields'] = ["name", "slug"]
        return context


# @method_decorator(login_required, name='dispatch')
class GenreDetailView(DetailView):
    model = Genre
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Жанр {context["object"]}'
        context["update_url"] = reverse_lazy("reviews:update_genre", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_genre", kwargs={"pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:genres')
        context['display_fields'] = ["name", "slug"]
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class GenreDeleteView(DeleteView):
    model = Genre
    success_url = reverse_lazy("reviews:genres")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genres'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['message'] = f'Удалить жанр {context["object"]}'
        context['cancel_url'] = reverse_lazy('reviews:genre_detail',  kwargs={"pk": self.object.pk})
        return context


review_context = {
    # 'create_url': 'reviews:create_review',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания
    'url_with_arg': True,

    # 'update_url': 'reviews:update_review',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования

    'action': 'Добавить отзыв',  # Для страницы списка
    # 'detail_url': 'reviews:review_detail',  # Для страницы списка

    # 'update_url': 'reviews:update_review',
    # 'delete_url': 'reviews:delete_review',
    'related_object_title': 'Комментарии',
    'no_related_objects_title': 'Комментариев нет',
    'create_related_object_title': 'Оставить комментарий',
}


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
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
        # context['title_id'] = title_id
        context['cancel_url'] = reverse_lazy('reviews:reviews',  kwargs={"title_id": title_id})
        context['create_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": title_id})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        title = Title.objects.get(pk=self.kwargs['title_id'])
        form.instance.title = title
        return super().form_valid(form)


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
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
        title_id = self.kwargs.get('title_id', 1)
        context['title'] = f'Список отзывов на произведение {Title.objects.get(pk=title_id)}'
        context['back_url'] = reverse_lazy('reviews:title_detail',  kwargs={"pk": title_id})
        context['create_url'] = reverse_lazy('reviews:create_review', kwargs={"title_id": title_id})
        context['display_fields'] = ["author", "text", "score", "pub_date"]
        pprint(context)
        return context

    def get_queryset(self):
        self.title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return Review.objects.filter(title=self.title)


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Отзыв {context["object"]}'
        self.title_id = self.kwargs['title_id']
        context['related_object_list'] = Comment.objects.filter(review_id=self.kwargs['pk'])
        context['create_related_object_url'] = reverse_lazy('reviews:create_comment', kwargs={'title_id': self.title_id, 'review_id': self.object.pk})
        pprint(context['create_related_object_url'])
        context["update_url"] = reverse_lazy("reviews:update_review", kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_review", kwargs={"title_id": self.object.title.pk, "pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:reviews',  kwargs={"title_id": self.object.title.pk})
        pprint("kwargs в get_context_data ReviewDetailView в create_related_object_url")
        pprint({'title_id': self.title_id, 'review_id': self.object.pk})
        pprint(context)
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
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


comment_context = {
    # 'create_url': 'reviews:create_review',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания
    # 'url_with_arg': True,

    # 'update_url': 'reviews:update_review',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования

    'action': 'Добавить комментарий',  # Для страницы списка
    # 'detail_url': 'reviews:review_detail',  # Для страницы списка

    # 'update_url': 'reviews:update_review',
    # 'delete_url': 'reviews:delete_review',
}


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'reviews/create_instance.html'
    form_class = CommentForm

    @property
    def title_id(self):
        return self.kwargs['title_id']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_success_url(self):
        return reverse_lazy(
            'reviews:review_detail', kwargs={'title_id': self.title_id, 'pk': self.review_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = 'Добавить комментарий'
        context['is_edit'] = False
        context['create_url'] = reverse_lazy('reviews:create_review', kwargs={'title_id': self.title_id, 'review_id': self.review_id})
        context['cancel_url'] = reverse_lazy('reviews:review_detail', kwargs={'title_id': self.title_id, 'pk': self.review_id})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        review = Review.objects.get(pk=self.kwargs['review_id'])
        form.instance.review = review
        return super().form_valid(form)


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'reviews/create_instance.html'

    @property
    def title_id(self):
        return self.kwargs['title_id']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = f'Изменить комментарий {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('reviews:comment_detail', kwargs={'title_id': self.title_id, 'review_id': self.review_id, "pk": self.object.pk})
        pprint(context)
        return context

    def get_success_url(self):
        return reverse_lazy('reviews:comment_detail', kwargs={'title_id': self.title_id, 'review_id': self.review_id, "pk": self.object.pk})


class CommentListView(ListView):
    model = Comment
    template_name = 'reviews/instances.html'

    @property
    def title_id(self):
        return self.kwargs['title_id']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = f'Список комментариев к отзыву {Review.objects.get(pk=self.review_id)}'
        context['back_url'] = reverse_lazy('reviews:review_detail',  kwargs={"title_id": self.title_id, "pk": self.review_id})
        context['create_url'] = reverse_lazy('reviews:create_comment', kwargs={'title_id': self.title_id, 'review_id': self.review_id})
        context['display_fields'] = ["author", "text", "pub_date"]
        pprint(context)
        return context

    def get_queryset(self):
        self.review = get_object_or_404(Review, id=self.review_id)
        return Comment.objects.filter(review=self.review)


class CommentDetailView(DetailView):
    model = Comment
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = f'Комментарий {context["object"]}'
        self.title_id = self.kwargs['title_id']
        self.review_id = self.kwargs['review_id']
        context["update_url"] = reverse_lazy("reviews:update_comment", kwargs={"title_id": self.title_id, "review_id": self.review_id, "pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_comment", kwargs={"title_id": self.title_id, "review_id": self.review_id, "pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:comments',  kwargs={"title_id": self.title_id, "review_id": self.review_id})
        context['display_fields'] = ["author", "text", "pub_date"]
        pprint(context)
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'reviews/confirm_delete.html'

    @property
    def title_id(self):
        return self.kwargs['title_id']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_success_url(self):
        return reverse_lazy('reviews:review_detail',  kwargs={'title_id': self.title_id, 'pk': self.review_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['message'] = f'Удалить комментарий {context["object"]}'
        context['cancel_url'] = reverse_lazy('reviews:comment_detail',  kwargs={'title_id': self.title_id, 'review_id': self.review_id, "pk": self.object.pk})
        return context

category_context = {
    # 'create_url': 'reviews:create_genre',  # Для страницы создания и редактирования
    'create_button_text': 'Добавить',  # Для страницы создания

    'update_url': 'reviews:update_category',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования
    'cancel_url': 'reviews:category_detail',  # Для страницы редактирования

    'action': 'Добавить категорию',  # Для страницы списка
    'detail_url': 'reviews:category_detail',  # Для страницы списка

    'back_url': 'reviews:categories',  # Для страницы деталей
    'update_url': 'reviews:update_category',
    'delete_url': 'reviews:delete_category',
}


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'reviews/create_instance.html'
    form_class = CategoryForm


    def get_success_url(self):
        return reverse_lazy(
            'reviews:categories'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = 'Добавить новую категорию'
        context['is_edit'] = False
        context["create_url"] = reverse_lazy("reviews:create_category")
        context['cancel_url'] = reverse_lazy('reviews:categories')
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'reviews/create_instance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = f'Изменить категорию {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy('reviews:category_detail',  kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:category_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CategoryListView(ListView):
    model = Category
    template_name = 'reviews/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = 'Список категорий'
        context["create_url"] = reverse_lazy("reviews:create_category")
        context['display_fields'] = ["name", "slug"]
        del context["back_url"]
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = f'Категория {context["object"]}'
        context["update_url"] = reverse_lazy("reviews:update_category", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("reviews:delete_category", kwargs={"pk": self.object.pk})
        context['back_url'] = reverse_lazy('reviews:categories')
        context['display_fields'] = ["name", "slug"]
        return context


@method_decorator(user_passes_test(is_admin_or_superuser), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("reviews:categories")
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:categories'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['message'] = f'Удалить категорию {context["object"]}'
        context['cancel_url'] = reverse_lazy('reviews:category_detail',  kwargs={"pk": self.object.pk})
        return context


class CabinetReviewsListView(ReviewListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Список отзывов'
        context['back_url'] = reverse_lazy('reviews:cabinet')
        context['display_fields'] = ["author", "text", "score", "pub_date"]
        del context["create_url"]
        pprint(context)
        return context

    def get_queryset(self):
        return Review.objects.all().order_by("-pk")
