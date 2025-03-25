from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

User = get_user_model()

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


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(
        'Genre', blank=True, related_name='genre')

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
        'Title', on_delete=models.CASCADE)
    text = models.TextField(max_length=1800)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return f'{self.author}: {self.text[:15]}...'

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
    text = models.TextField(max_length=1800)
    pub_date = models.DateTimeField(auto_now_add=True)
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
        return f'{self.author}: {self.text[:15]}...'

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
