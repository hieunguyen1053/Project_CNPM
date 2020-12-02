from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name='api-receipt-all'),
    path('create', views.create, name='api-receipt-create'),
    path('<int:id>/delete', views.delete, name='api-receipt-delete'),
]