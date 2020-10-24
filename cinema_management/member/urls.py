from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-member-all'),
    path('create', views.create, name='api-member-create'),
    path('<int:id>', views.get, name='api-member-detail'),
    path('<int:id>/edit', views.edit, name='api-member-edit'),
    path('<int:id>/delete', views.delete, name='api-member-delete'),
]