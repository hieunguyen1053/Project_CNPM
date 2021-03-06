from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-combo-all'),
    path('create', views.create, name='api-combo-create'),
    path('<int:id>', views.get, name='api-combo-detail'),
    path('<int:id>/edit', views.edit, name='api-combo-edit'),
    path('<int:id>/delete', views.delete, name='api-combo-delete'),
]