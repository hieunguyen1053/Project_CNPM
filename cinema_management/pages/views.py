from auditorium.models import Auditorium
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from movie.models import Movie


# Create your views here
def home(request):
    return render(request, 'home/index.html')

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('admin-movie')
        else:
            return render(request, 'signin.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin-movie')
            if user.is_staff:
                return redirect('admin-movie')
        else:
            return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def admin_movie(request):
    if not request.user.is_superuser:
        return redirect('login')
    context = {
        "LANGUAGE_MAP": Movie.LANGUAGE_MAP,
        "GENRES_MAP": Movie.GENRES_MAP,
        "RATE_MAP": Movie.RATE_MAP,
    }
    return render(request, 'movie/admin.html', context)

def admin_auditorium(request):
    if not request.user.is_superuser:
        return redirect('login')
    context = {
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'auditorium/admin.html', context)

def admin_schedule(request):
    if not request.user.is_superuser:
        return redirect('login')
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

def admin_member(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'member/admin.html')

def admin_staff(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'staff/admin.html')
