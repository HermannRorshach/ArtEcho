from django.urls import path

from users.views import UsersListView

from . import views

app_name = 'admin_office'

urlpatterns = [
    path('cabinet', views.CabinetView.as_view(), name='cabinet'),
    path(
        'cabinet/reviews',
        views.CabinetReviewsListView.as_view(), name='cabinet_reviews'),
    path(
        'cabinet/comments',
        views.CabinetCommentListView.as_view(), name='cabinet_comments'),
    path(
        'cabinet/user/new/',
        views.UserCreateView.as_view(), name='create_user'),
    path('cabinet/users/', UsersListView.as_view(), name='users'),
    path(
        'cabinet/user/<slug:username>/',
        views.CabinetUserDetailView.as_view(), name='admin_user_detail'),
    path(
        'cabinet/user/update/<slug:username>/',
        views.CabinetUserUpdateView.as_view(), name='admin_update_user'),
    path(
        'cabinet/user/delete/<slug:username>/',
        views.CabinetUserDeleteView.as_view(), name='admin_delete_user'),

]
