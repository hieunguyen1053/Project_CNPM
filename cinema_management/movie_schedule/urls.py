from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-schedule-all'),
    path('create', views.create, name='api-schedule-create'),
    path('<int:id>', views.get, name='api-schedule-detail'),
    path('<int:id>/edit', views.edit, name='api-schedule-edit'),
    path('<int:id>/delete', views.delete, name='api-schedule-delete'),
]