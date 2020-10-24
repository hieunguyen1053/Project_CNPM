from django.shortcuts import render
from movie.models import Movie
from auditorium.models import Auditorium

# Create your views here
def home(request):
    return render(request, 'home/index.html')

def admin_movie(request):
    context = {
        "LANGUAGE_MAP": Movie.LANGUAGE_MAP,
        "GENRES_MAP": Movie.GENRES_MAP,
        "RATE_MAP": Movie.RATE_MAP,
    }
    return render(request, 'movie/admin.html', context)

def admin_auditorium(request):
    context = {
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'auditorium/admin.html', context)

def admin_schedule(request):
    movies = Movie.objects.all()
    movies = movies.filter(status=True)
    auditoriums = Auditorium.objects.all()
    auditoriums = sorted(auditoriums, key=lambda auditorium: auditorium.name)
    context = {
        "movies": movies,
        "auditoriums": auditoriums,
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'schedule/admin.html', context)