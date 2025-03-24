from django import forms
from .models import Comment, Category, Title, Genre, Review


class TitleForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = ("name", "year", "category", "genre")


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ("name", "slug")


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("text", "score")
