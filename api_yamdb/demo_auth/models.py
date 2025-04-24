from django.db import models


class IsDemoFieldModel(models.Model):
    """
    Абстрактная модель, добавляющая поле is_demo во все классы-наследники.
    """
    is_demo = models.BooleanField(default=False)

    class Meta:
        abstract = True
