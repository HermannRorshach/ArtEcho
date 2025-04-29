from django.urls import path

from . import views

app_name = 'demo_auth'

urlpatterns = [
    path(
        'demo_auth/',
        views.DemoUserLoginView.as_view(),
        name='demo_auth'),
]
