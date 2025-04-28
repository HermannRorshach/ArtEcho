from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    list_display_links = ('pk',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    list_display_links = ('pk',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'text', 'author', 'score', 'slug'
    )
    list_editable = ('title', 'text', 'score', 'slug')
    list_display_links = ('pk',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'text', 'author', 'slug'
    )
    list_editable = ('text', 'slug')
    list_display_links = ('pk',)