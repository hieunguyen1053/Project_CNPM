from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-movie-all'),
    path('create', views.create, name='api-movie-create'),
    path('<int:id>', views.get, name='api-movie-detail'),
    path('<int:id>/edit', views.edit, name='api-movie-edit'),
    path('<int:id>/delete', views.delete, name='api-movie-delete'),
]