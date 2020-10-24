from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-auditorium-all'),
    path('create', views.create, name='api-auditorium-create'),
    path('<int:id>', views.get, name='api-auditorium-detail'),
    path('<int:id>/edit', views.edit, name='api-auditorium-edit'),
    path('<int:id>/delete', views.delete, name='api-auditorium-delete'),
]