from datetime import datetime

from demo_auth.models import IsDemoFieldModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg, IntegerField
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

User = get_user_model()


def cut_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text


class SlugModel(IsDemoFieldModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            source_text = (
                getattr(self, 'text', None)
                or getattr(self, 'name', None)
            )
            transliterated = translit(source_text[:30], 'ru', reversed=True)
            base_slug = slugify(transliterated)

            self.slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


class Category(SlugModel):
    name = models.CharField(
        max_length=100, verbose_name='Имя категории')
    slug = models.SlugField(
        max_length=255, verbose_name='Относительная ссылка',
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')],
        unique=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews:category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugModel):
    name = models.CharField(
        max_length=100, verbose_name='Имя жанра')
    slug = models.SlugField(
        max_length=255,
        verbose_name='Относительная ссылка',
        validators=[RegexValidator(
            regex='^[-a-zA-Z0-9_]+$')],
        unique=True,)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews:genre_detail', kwargs={'slug': self.slug})


class Title(SlugModel):
    name = models.CharField(
        max_length=100, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год создания')
    description = models.TextField(max_length=1800, blank=True, null=True)
    slug = models.SlugField(max_length=255,
                            verbose_name='Ссылка',
                            validators=[RegexValidator(
                                regex='^[-a-zA-Z0-9_]+$')],
                            unique=True,)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',)
    genre = models.ManyToManyField(
        'Genre', blank=True, related_name='genre',
        verbose_name='Жанр',)

    @property
    def average_rating(self):
        """
        Вычисляет средний рейтинг произведения на основе связанных отзывов.
        Возвращает 0, если отзывов нет.
        """
        return self.reviews.aggregate(
            avg_rating=Coalesce(Avg('score'),
                                None, output_field=IntegerField())
        )['avg_rating']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews:title_detail', kwargs={'slug': self.slug})

    def clean(self):
        if self.year > datetime.now().year:
            raise ValidationError(
                {'year': 'Год не может быть больше текущего'})


class Review(SlugModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Автор',
        help_text='Автор отзыва'
    )
    title = models.ForeignKey(
        'Title', related_name='reviews', on_delete=models.CASCADE,
        verbose_name='Произведение')
    text = models.TextField(max_length=1800)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)],
                                verbose_name='Оценка пользователя')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время публикации')
    update_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')
    slug = models.SlugField(max_length=255, verbose_name='Ссылка',
                            validators=[RegexValidator(
                                regex='^[-a-zA-Z0-9_]+$')],
                            unique=True,)

    def __str__(self):
        return (f'Отзыв {self.author} на произведение {self.title}:\n'
                f'{cut_text(self.text, 25)}')

    def title_link(self):
        path = reverse('reviews:title_detail', kwargs={'slug': self.title.slug})
        return f'<a href="{path}">{self.title}:</a>'

    def str_with_link(self):
        return f'Отзыв {self.author} на {self.title_link()}'


    def get_absolute_url(self):
        return reverse(
            'reviews:review_detail',
            kwargs={'title_slug': self.title.slug, 'pk': self.pk})

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(SlugModel):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE)
    text = models.TextField(max_length=1800, verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment', verbose_name='Автор',
        help_text='Автор комментария',
        default=100
    )
    slug = models.SlugField(max_length=255,
                            verbose_name='Ссылка',
                            validators=[RegexValidator(
                                regex='^[-a-zA-Z0-9_]+$')],
                            # unique=True,
                            blank=True, null=True)

    def __str__(self):
        return (f'Комментарий {self.author} к отзыву {self.review.author} '
                f'на произведение {self.review.title}:\n'
                f'{cut_text(self.text, 25)}')

    def get_absolute_url(self):
        return reverse('reviews:comment_detail', kwargs={
            'title_slug': self.review.title.slug,
            'review_id': self.review.pk,
            'pk': self.pk
        })

    def title_link(self):
        path = reverse(
            'reviews:title_detail', kwargs={'slug': self.review.title.slug})
        return f'<a href="{path}">произведение:</a>'

    def review_link(self):
        path = reverse(
            'reviews:review_detail',
            kwargs={'title_slug': self.review.title.slug, 'pk': self.review.pk})
        return f'<a href="{path}">отзыву:</a>'

    def str_with_link(self):
        return (f'Комментарий {self.author} к {self.review_link()}<br>'
                f'на {self.title_link()}<br>{cut_text(self.text, 25)}')
