from django import forms
from .models import Comment, Category, Title, Genre, Review


class TitleForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = ("name", "year", "category", "genre")