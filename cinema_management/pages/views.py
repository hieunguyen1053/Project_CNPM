from django.shortcuts import render
from movie.models import Movie

# Create your views here
def home(request):
    return render(request, 'home/index.html')

def movie(request):
    context = {
        "LANGUAGE_MAP": Movie.LANGUAGE_MAP,
        "GENRES_MAP": Movie.GENRES_MAP,
        "RATE_MAP": Movie.RATE_MAP,
    }
    return render(request, 'movie/index.html', context)