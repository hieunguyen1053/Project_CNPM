from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('admin/movie', views.admin_movie, name='admin-movie'),
    path('admin/auditorium', views.admin_auditorium, name='admin-auditorium'),
    path('admin/schedule', views.admin_schedule, name='admin-schedule'),
    path('admin/member', views.admin_member, name='admin-member'),
    path('admin/staff', views.admin_staff, name='admin-staff'),
    path('movie', views.movie, name='movie'),
]