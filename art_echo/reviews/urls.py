from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path(
        'contacts/',
        views.ContactsView.as_view(),
        name='contacts'),
    path(
        'faq/',
        views.FaqView.as_view(),
        name='faq'),
    path('title/new/', views.TitleCreateView.as_view(), name='create_title'),
    path(
        'title/update/<slug:slug>/',
        views.TitleUpdateView.as_view(), name='update_title'),
    path('', views.TitleListView.as_view(), name='titles'),
    path(
        'title/<slug:slug>/',
        views.TitleDetailView.as_view(), name='title_detail'),
    path(
        'title/delete/<slug:slug>/',
        views.TitleDeleteView.as_view(), name='delete_title'),

    path('genre/new/', views.GenreCreateView.as_view(), name='create_genre'),
    path(
        'genre/update/<slug:slug>/',
        views.GenreUpdateView.as_view(), name='update_genre'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path(
        'genre/<slug:slug>/',
        views.GenreDetailView.as_view(), name='genre_detail'),
    path(
        'genre/delete/<slug:slug>/',
        views.GenreDeleteView.as_view(), name='delete_genre'),

    path(
        'category/new/',
        views.CategoryCreateView.as_view(), name='create_category'),
    path(
        'category/update/<slug:slug>/',
        views.CategoryUpdateView.as_view(), name='update_category'),
    path(
        'categories/', views.CategoryListView.as_view(), name='categories'),
    path(
        'category/<slug:slug>/',
        views.CategoryDetailView.as_view(), name='category_detail'),
    path(
        'category/delete/<slug:slug>/',
        views.CategoryDeleteView.as_view(), name='delete_category'),

    path(
        'title/<slug:title_slug>/review/new/',
        views.ReviewCreateView.as_view(), name='create_review'),
    path(
        'title/<slug:title_slug>/review/update/<int:pk>/',
        views.ReviewUpdateView.as_view(), name='update_review'),
    path(
        'title/<slug:title_slug>/reviews/',
        views.ReviewListView.as_view(), name='reviews'),
    path(
        'title/<slug:title_slug>/review/<int:pk>/',
        views.ReviewDetailView.as_view(), name='review_detail'),
    path(
        'title/<slug:title_slug>/review/delete/<int:pk>/',
        views.ReviewDeleteView.as_view(), name='delete_review'),

    path(
        'title/<slug:title_slug>/review/<int:review_id>/comment/new/',
        views.CommentCreateView.as_view(), name='create_comment'),
    path(
        'title/<slug:title_slug>/review/<int:review_id>/'
        'comment/update/<int:pk>/',
        views.CommentUpdateView.as_view(), name='update_comment'),
    path(
        'title/<slug:title_slug>/review/<int:review_id>/comments/',
        views.CommentListView.as_view(), name='comments'),
    path(
        'title/<slug:title_slug>/review/<int:review_id>/'
        'comment/<int:pk>/',
        views.CommentDetailView.as_view(), name='comment_detail'),
    path(
        'title/<slug:title_slug>/review/<int:review_id>/'
        'comment/delete/<int:pk>/',
        views.CommentDeleteView.as_view(), name='delete_comment'),
]
