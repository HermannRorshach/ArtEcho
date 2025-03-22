from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views



app_name = 'reviews'

urlpatterns = [
    path('title/new/', views.TitleCreateView.as_view(), name='create_title'),
    path('title/update/<int:pk>/', views.TitleUpdateView.as_view(), name='update_title'),
    path('title/', views.TitleListView.as_view(), name='titles'),
    path('title/<int:pk>/', views.TitleDetailView.as_view(), name='title_detail'),
    path('title/delete/<int:pk>/', views.TitleDeleteView.as_view(), name='delete_title'),

]
