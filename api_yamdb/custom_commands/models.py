from django.db import models


class TestCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
