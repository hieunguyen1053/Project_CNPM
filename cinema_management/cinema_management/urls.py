"""cinema_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('root/', admin.site.urls),
    path('api/v1/movie/', include('movie.urls')),
    path('api/v1/combo/', include('combo.urls')),
    path('api/v1/auditorium/', include('auditorium.urls')),
    path('api/v1/schedule/', include('movie_schedule.urls')),
    path('api/v1/member/', include('member.urls')),
    path('api/v1/staff/', include('staff.urls')),
    path('api/v1/receipt/', include('receipt.urls')),
] + static(settings.STATIC_URL)
