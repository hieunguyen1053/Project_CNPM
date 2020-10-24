from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='movies'),
    path('create', views.create, name='movie-create'),
    path('<int:id>', views.get, name='movie-detail'),
    path('<int:id>/edit', views.edit, name='movie-edit'),
    path('<int:id>/delete', views.delete, name='movie-delete'),
]