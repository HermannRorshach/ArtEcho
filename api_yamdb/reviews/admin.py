from django.contrib import admin
from .models import Category


@admin.register(Category)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
