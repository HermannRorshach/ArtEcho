from django.conf import settings
from django.conf.urls.static import static
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
    # path("titles/<int:title_id>/reviews/create/", views.ReviewCreateView.as_view(), name="review_create"),
    # path("titles/<int:title_id>/reviews/", views.ReviewListView.as_view(), name="review_list"),
    path('title/new/', views.TitleCreateView.as_view(), name='create_title'),
    path('title/update/<int:pk>/', views.TitleUpdateView.as_view(), name='update_title'),
    path('', views.TitleListView.as_view(), name='titles'),
    path('title/<int:pk>/', views.TitleDetailView.as_view(), name='title_detail'),
    path('title/delete/<int:pk>/', views.TitleDeleteView.as_view(), name='delete_title'),

    path('genre/new/', views.GenreCreateView.as_view(), name='create_genre'),
    path('genre/update/<int:pk>/', views.GenreUpdateView.as_view(), name='update_genre'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/delete/<int:pk>/', views.GenreDeleteView.as_view(), name='delete_genre'),

    path('title/<int:title_id>/review/new/', views.ReviewCreateView.as_view(), name='create_review'),
    path('title/<int:title_id>/review/update/<int:pk>/', views.ReviewUpdateView.as_view(), name='update_review'),
    path('title/<int:title_id>/reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('title/<int:title_id>/review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('title/<int:title_id>/review/delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='delete_review'),

    path('title/<int:title_id>/review/<int:review_id>/comment/new/', views.CommentCreateView.as_view(), name='create_comment'),
    path('title/<int:title_id>/review/<int:review_id>/comment/update/<int:pk>/', views.CommentUpdateView.as_view(), name='update_comment'),
    path('title/<int:title_id>/review/<int:review_id>/comments/', views.CommentListView.as_view(), name='comments'),
    path('title/<int:title_id>/review/<int:review_id>/comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('title/<int:title_id>/review/<int:review_id>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),

]
