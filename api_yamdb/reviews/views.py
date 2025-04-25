from demo_auth.mixins import DemoAccessMixin, DemoFormMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CategoryForm, CommentForm, GenreForm, ReviewForm, TitleForm
from .models import Category, Comment, Genre, Review, Title
from .utils import (AuthorOrPrivilegedRequiredMixin, IsAdminOrSuperuser,
                    IsStaffMixin)


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
    'create_button_text': 'Добавить',  # Для страницы создания

    'update_url': 'reviews:update_title',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования

    'action': 'Добавить произведение',  # Для страницы списка
    'detail_url': 'reviews:title_detail',  # Для страницы списка

    'update_url': 'reviews:update_title',
    'delete_url': 'reviews:delete_title',
    'related_object_title': 'Отзывы',
    'no_related_objects_title': 'Отзывов нет',
    'create_related_object_title': 'Оставить отзыв',
}


class TitleCreateView(IsAdminOrSuperuser, DemoAccessMixin, DemoFormMixin, CreateView):
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
        return context


class TitleUpdateView(IsAdminOrSuperuser, DemoAccessMixin, DemoFormMixin, UpdateView):
    model = Title
    form_class = TitleForm
    template_name = 'reviews/create_instance.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = f'Изменить произведение {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'reviews:title_detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:title_detail', kwargs={'slug': self.kwargs['slug']}
        )


class TitleListView(DemoAccessMixin, ListView):
    model = Title
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по жанру (если параметр есть)
        if genre_id := self.request.GET.get('genre'):
            return queryset.filter(genre__id=genre_id)

        # Фильтрация по категории (если параметр есть)
        if category_id := self.request.GET.get('category'):
            return queryset.filter(category__id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = 'Список произведений'
        if IsAdminOrSuperuser.check_permission(self.request.user):
            context['create_url'] = reverse_lazy('reviews:create_title')
        context['genres_list'] = Genre.objects.all()
        context['category_list'] = Category.objects.all()
        context['display_fields'] = ['year', 'category', 'genre']
        context['includes'] = ['reviews/includes/rating.html']
        return context


class TitleDetailView(DemoAccessMixin, DetailView):
    model = Title
    template_name = 'reviews/instance_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['title'] = f'Произведение {context["object"]}'
        context['related_object_list'] = Review.objects.filter(
            title__slug=self.kwargs['slug'])
        context['create_related_object_url'] = reverse_lazy(
            'reviews:create_review', kwargs={'title_slug': self.object.slug})
        context['update_url'] = reverse_lazy(
            'reviews:update_title', kwargs={'slug': self.object.slug})
        context['delete_url'] = reverse_lazy(
            'reviews:delete_title', kwargs={'slug': self.object.slug})
        context['back_url'] = reverse_lazy('reviews:titles')
        context['display_fields'] = ['year', 'category', 'genre']
        context['includes'] = ['reviews/includes/rating.html']
        context['average_rating'] = context['object'].average_rating
        context['can_edit'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        context['can_delete'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        return context


class TitleDeleteView(IsAdminOrSuperuser, DemoAccessMixin, DeleteView):
    model = Title
    success_url = reverse_lazy('reviews:titles')
    template_name = 'reviews/confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:titles'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title_context)
        context['cancel_url'] = reverse_lazy(
            'reviews:title_detail', kwargs={'slug': self.object.slug})
        return context


genre_context = {
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


class GenreCreateView(IsAdminOrSuperuser, DemoAccessMixin, CreateView):
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
        context['cancel_url'] = reverse_lazy('reviews:genres')
        return context


class GenreUpdateView(IsAdminOrSuperuser, DemoAccessMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'reviews/create_instance.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Изменить жанр {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'reviews:genre_detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genre_detail', kwargs={'slug': self.kwargs['slug']}
        )


class GenreListView(IsStaffMixin, DemoAccessMixin, ListView):
    model = Genre
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = 'Список жанров'
        if IsAdminOrSuperuser.check_permission(self.request.user):
            context['create_url'] = reverse_lazy('reviews:create_genre')
        del context['back_url']
        context['display_fields'] = ['name', 'slug']
        return context


class GenreDetailView(IsStaffMixin, DemoAccessMixin, DetailView):
    model = Genre
    template_name = 'reviews/instance_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['title'] = f'Жанр {context["object"]}'
        context['update_url'] = reverse_lazy(
            'reviews:update_genre', kwargs={'slug': self.object.slug})
        context['delete_url'] = reverse_lazy(
            'reviews:delete_genre', kwargs={'slug': self.object.slug})
        context['back_url'] = reverse_lazy('reviews:genres')
        context['display_fields'] = ['name', 'slug']
        context['can_edit'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        context['can_delete'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        return context


class GenreDeleteView(IsAdminOrSuperuser, DemoAccessMixin, DeleteView):
    model = Genre
    success_url = reverse_lazy('reviews:genres')
    template_name = 'reviews/confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:genres'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(genre_context)
        context['cancel_url'] = reverse_lazy(
            'reviews:genre_detail', kwargs={'slug': self.object.slug})
        return context


review_context = {
    'create_button_text': 'Добавить',  # Для страницы создания
    'url_with_arg': True,
    'update_button_text': 'Изменить',  # Для страницы редактирования
    'action': 'Добавить отзыв',  # Для страницы списка
    'related_object_title': 'Комментарии',
    'no_related_objects_title': 'Комментариев нет',
    'create_related_object_title': 'Оставить комментарий',
    'avatar': True,
}


@method_decorator(login_required, name='dispatch')
class ReviewCreateView(DemoAccessMixin, CreateView):
    model = Review
    template_name = 'reviews/create_instance.html'
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        title_slug = self.kwargs['title_slug']
        # Проверяем, есть ли уже отзыв у пользователя
        existing_review = Review.objects.filter(
            title__slug=title_slug,
            author=request.user
        ).first()

        if existing_review:
            return redirect(
                'reviews:update_review',
                title_slug=title_slug, pk=existing_review.pk)

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        title_slug = self.kwargs['title_slug']
        return reverse_lazy(
            'reviews:reviews', kwargs={'title_slug': title_slug}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = 'Добавить новый отзыв'
        context['is_edit'] = False
        title_slug = self.kwargs['title_slug']
        context['cancel_url'] = reverse_lazy(
            'reviews:reviews', kwargs={'title_slug': title_slug})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        title = Title.objects.get(slug=self.kwargs['title_slug'])
        form.instance.title = title
        return super().form_valid(form)


class ReviewUpdateView(AuthorOrPrivilegedRequiredMixin, DemoAccessMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_instance.html'
    # template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Изменить отзыв {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.object.title.slug, 'pk': self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.object.title.slug, 'pk': self.object.pk}
        )


class ReviewListView(DemoAccessMixin, ListView):
    model = Review
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        title_slug = self.kwargs.get('title_slug')
        if title_slug:
            title = get_object_or_404(Title, slug=title_slug)
            context['title'] = f'Список отзывов на произведение {title}'
        context['back_url'] = reverse_lazy(
            'reviews:title_detail', kwargs={'slug': title_slug})
        context['create_url'] = reverse_lazy(
            'reviews:create_review', kwargs={'title_slug': title_slug})
        context['display_fields'] = ['author', 'text', 'score', 'pub_date']
        return context

    def get_queryset(self):
        self.title = get_object_or_404(Title, slug=self.kwargs['title_slug'])
        queryset = Review.objects.filter(title=self.title)
        return self.filter_queryset(queryset)


class ReviewDetailView(DemoAccessMixin, DetailView):
    model = Review
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['title'] = f'Отзыв {context["object"]}'
        self.title_slug = self.kwargs['title_slug']
        context['related_object_list'] = Comment.objects.filter(
            review_id=self.kwargs['pk'])
        context['create_related_object_url'] = reverse_lazy(
            'reviews:create_comment',
            kwargs={'title_slug': self.title_slug, 'review_id': self.object.pk})
        context['update_url'] = reverse_lazy(
            'reviews:update_review',
            kwargs={'title_slug': self.object.title.slug, 'pk': self.object.pk})
        context['delete_url'] = reverse_lazy(
            'reviews:delete_review',
            kwargs={'title_slug': self.object.title.slug, 'pk': self.object.pk})
        context['back_url'] = reverse_lazy(
            'reviews:reviews', kwargs={'title_slug': self.object.title.slug})
        context['display_fields'] = ['author', 'text', 'score', 'pub_date']
        context['can_edit'] = AuthorOrPrivilegedRequiredMixin.check_permission(
            self.request.user,
            context['object']
        )
        context['can_delete'] = AuthorOrPrivilegedRequiredMixin.check_permission(
            self.request.user,
            context['object']
        )
        return context


class ReviewDeleteView(AuthorOrPrivilegedRequiredMixin, DemoAccessMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('reviews:reviews')
    template_name = 'reviews/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:reviews', kwargs={'title_slug': self.object.title.slug}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(review_context)
        context['cancel_url'] = reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.object.title.slug, 'pk': self.object.pk})
        return context


comment_context = {
    'create_button_text': 'Добавить',  # Для страницы создания
    # 'url_with_arg': True,

    # 'update_url': 'reviews:update_review',  # Для страницы редактирования
    'update_button_text': 'Изменить',  # Для страницы редактирования

    'action': 'Добавить комментарий',  # Для страницы списка
    # 'detail_url': 'reviews:review_detail',  # Для страницы списка

    # 'update_url': 'reviews:update_review',
    # 'delete_url': 'reviews:delete_review',
    'avatar': True,
}


@method_decorator(login_required, name='dispatch')
class CommentCreateView(DemoAccessMixin, CreateView):
    model = Comment
    template_name = 'reviews/create_instance.html'
    form_class = CommentForm

    @property
    def title_slug(self):
        return self.kwargs['title_slug']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_success_url(self):
        return reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.title_slug, 'pk': self.review_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = 'Добавить комментарий'
        context['is_edit'] = False
        context['create_url'] = reverse_lazy(
            'reviews:create_review',
            kwargs={'title_slug': self.title_slug, 'review_id': self.review_id})
        context['cancel_url'] = reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.title_slug, 'pk': self.review_id})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        review = Review.objects.get(pk=self.kwargs['review_id'])
        form.instance.review = review
        return super().form_valid(form)


class CommentUpdateView(AuthorOrPrivilegedRequiredMixin, DemoAccessMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'reviews/create_instance.html'

    @property
    def title_slug(self):
        return self.kwargs['title_slug']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = f'Изменить комментарий {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'reviews:comment_detail',
            kwargs={
                'title_slug': self.title_slug, 'review_id': self.review_id,
                'pk': self.object.pk})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:comment_detail',
            kwargs={'title_slug': self.title_slug, 'review_id': self.review_id,
                    'pk': self.object.pk})


class CommentListView(DemoAccessMixin, ListView):
    model = Comment
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE

    @property
    def title_slug(self):
        return self.kwargs.get('title_slug', 1)

    @property
    def review_id(self):
        return self.kwargs.get('review_id', 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = (f'Список комментариев к отзыву '
                            f'{Review.objects.get(pk=self.review_id)}')
        context['back_url'] = reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.title_slug, 'pk': self.review_id})
        context['create_url'] = reverse_lazy(
            'reviews:create_comment',
            kwargs={'title_slug': self.title_slug, 'review_id': self.review_id})
        context['display_fields'] = ['author', 'text', 'pub_date']
        return context

    def get_queryset(self):
        self.review = get_object_or_404(Review, id=self.review_id)
        queryset = Comment.objects.filter(review=self.review)
        return self.filter_queryset(queryset)


class CommentDetailView(DemoAccessMixin, DetailView):
    model = Comment
    template_name = 'reviews/instance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['title'] = f'Комментарий {context["object"]}'
        self.title_slug = self.kwargs['title_slug']
        self.review_id = self.kwargs['review_id']
        context['update_url'] = reverse_lazy(
            'reviews:update_comment',
            kwargs={
                'title_slug': self.title_slug, 'review_id': self.review_id,
                'pk': self.object.pk})
        context['delete_url'] = reverse_lazy(
            'reviews:delete_comment',
            kwargs={'title_slug': self.title_slug,
                    'review_id': self.review_id, 'pk': self.object.pk})
        context['back_url'] = reverse_lazy(
            'reviews:comments',
            kwargs={'title_slug': self.title_slug, 'review_id': self.review_id})
        context['display_fields'] = ['author', 'text', 'pub_date']

        context['can_edit'] = AuthorOrPrivilegedRequiredMixin.check_permission(
            self.request.user,
            context['object']
        )
        context['can_delete'] = AuthorOrPrivilegedRequiredMixin.check_permission(
            self.request.user,
            context['object']
        )
        return context


class CommentDeleteView(AuthorOrPrivilegedRequiredMixin, DemoAccessMixin, DeleteView):
    model = Comment
    template_name = 'reviews/confirm_delete.html'

    @property
    def title_slug(self):
        return self.kwargs['title_slug']

    @property
    def review_id(self):
        return self.kwargs['review_id']

    def get_success_url(self):
        return reverse_lazy(
            'reviews:review_detail',
            kwargs={'title_slug': self.title_slug, 'pk': self.review_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(comment_context)
        context['cancel_url'] = reverse_lazy(
            'reviews:comment_detail',
            kwargs={
                'title_slug': self.title_slug, 'review_id': self.review_id,
                'pk': self.object.pk})
        return context


category_context = {
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


class CategoryCreateView(IsAdminOrSuperuser, DemoAccessMixin, CreateView):
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
        context['cancel_url'] = reverse_lazy('reviews:categories')
        return context


class CategoryUpdateView(IsAdminOrSuperuser, DemoAccessMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'reviews/create_instance.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = f'Изменить категорию {context["object"]}'
        context['is_edit'] = True
        context['cancel_url'] = reverse_lazy(
            'reviews:category_detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy(
            'reviews:category_detail', kwargs={'slug': self.kwargs['slug']}
        )


class CategoryListView(IsStaffMixin, DemoAccessMixin, ListView):
    model = Category
    template_name = 'reviews/instances.html'
    paginate_by = settings.PAGINATION_PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = 'Список категорий'
        if IsAdminOrSuperuser.check_permission(self.request.user):
            context['create_url'] = reverse_lazy('reviews:create_category')
        context['display_fields'] = ['name', 'slug']
        del context['back_url']
        return context


class CategoryDetailView(IsStaffMixin, DemoAccessMixin, DetailView):
    model = Category
    template_name = 'reviews/instance_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['title'] = f'Категория {context["object"]}'
        context['update_url'] = reverse_lazy(
            'reviews:update_category', kwargs={'slug': self.object.slug})
        context['delete_url'] = reverse_lazy(
            'reviews:delete_category', kwargs={'slug': self.object.slug})
        context['back_url'] = reverse_lazy('reviews:categories')
        context['display_fields'] = ['name', 'slug']
        context['can_edit'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        context['can_delete'] = IsAdminOrSuperuser.check_permission(
            self.request.user
        )
        return context


class CategoryDeleteView(IsAdminOrSuperuser, DemoAccessMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('reviews:categories')
    template_name = 'reviews/confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy(
            'reviews:categories'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category_context)
        context['cancel_url'] = reverse_lazy(
            'reviews:category_detail', kwargs={'slug': self.object.slug})
        return context
