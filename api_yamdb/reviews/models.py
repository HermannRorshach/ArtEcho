from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

User = get_user_model()

def cut_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reviews:genre_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_slug = translit(self.name, 'ru', reversed=True)
            self.slug = slugify(transliterated_slug)
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.CharField(max_length=100,
        verbose_name='Название')
    year = models.IntegerField(verbose_name='Год создания',)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',)
    genre = models.ManyToManyField(
        'Genre', blank=True, related_name='genre',
        verbose_name='Жанр',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reviews:title_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_slug = translit(self.name, 'ru', reversed=True)
            self.slug = slugify(transliterated_slug)
        super().save(*args, **kwargs)


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Автор',
        help_text='Автор отзыва'
    )
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, verbose_name='Произведение')
    text = models.TextField(max_length=1800)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)],
                                verbose_name='Оценка пользователя')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время публикации')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    slug = models.SlugField(max_length=255, verbose_name='Ссылка')

    def __str__(self):
        return (f"Отзыв {self.author} на произведение {self.title}:\n"
                f"{cut_text(self.text, 25)}")

    def get_absolute_url(self):
        return reverse("reviews:review_detail", kwargs={"title_id": self.title.pk, "pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_slug = translit(self.text[:15], 'ru', reversed=True)
            self.slug = slugify(transliterated_slug)
        super().save(*args, **kwargs)


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE)
    text = models.TextField(max_length=1800, verbose_name='Текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment', verbose_name='Автор',
        help_text='Автор комментария',
        default=100
    )
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return (f"Комментарий {self.author} к отзыву {self.review.author} "
                f"на произведение {self.review.title}:\n{cut_text(self.text, 25)}")

    def get_absolute_url(self):
        return reverse("reviews:comment_detail", kwargs={
            "title_id": self.review.title.pk,
            "review_id": self.review.pk,
            "pk": self.pk
        })


    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_slug = translit(self.text[:15], 'ru', reversed=True)
            self.slug = slugify(transliterated_slug)
        super().save(*args, **kwargs)
