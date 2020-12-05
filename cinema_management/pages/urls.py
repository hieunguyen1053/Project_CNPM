from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('admin', views.dashboard, name='admin-dashboard'),
    path('admin/movie', views.admin_movie, name='admin-movie'),
    path('admin/auditorium', views.admin_auditorium, name='admin-auditorium'),
    path('admin/schedule', views.admin_schedule, name='admin-schedule'),
    path('admin/member', views.admin_member, name='admin-member'),
    path('admin/combo', views.admin_combo, name='admin-combo'),
    path('admin/staff', views.admin_staff, name='admin-staff'),
    path('admin/receipt', views.admin_receipt, name='admin-receipt'),
    path('movie', views.movie, name='movie'),
    path('movie/<int:id>', views.movie_detail, name='movie-detail'),
    path('booking/<int:id>/seats', views.booking_seats, name='booking-seats'),
    path('booking/<int:id>/combos', views.booking_combos, name='booking-combos'),
    path('booking/<int:id>/check', views.booking_check, name='booking-check'),
    path('add-member', views.add_member, name='add-member'),
    path('combo', views.combo_list, name='combo-list'),
    path('combo/check', views.combo_check, name='combo-check'),
]