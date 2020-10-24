from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/movie', views.admin_movie, name='admin-movie'),
    path('admin/auditorium', views.admin_auditorium, name='admin-auditorium'),
    path('admin/schedule', views.admin_schedule, name='admin-schedule'),
]