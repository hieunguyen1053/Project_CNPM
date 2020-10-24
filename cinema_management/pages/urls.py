from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/movie', views.movie, name='admin-movie'),
]