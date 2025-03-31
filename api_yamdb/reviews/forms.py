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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("text", "score")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
