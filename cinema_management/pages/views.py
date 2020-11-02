from auditorium.models import Auditorium
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from movie.models import Movie
from movie_schedule.models import MovieSchedule
import datetime

# Create your views here
def home(request):
    return render(request, 'home/index.html')

def login_view(request):
    if request.method == "GET":
        if request.user.is_superuser:
            return redirect('admin-movie')
        if request.user.is_staff:
            return redirect('movie')
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
                return redirect('movie')
        else:
            return redirect('login')

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

def movie(request):
    if not request.user.is_authenticated:
        return redirect('login')
    movies = Movie.objects.all()
    movies = movies.filter(status=True)
    context = {
        "movies": movies,
        "LANGUAGE_MAP": Movie.LANGUAGE_MAP,
        "GENRES_MAP": Movie.GENRES_MAP,
        "RATE_MAP": Movie.RATE_MAP,
    }
    return render(request, 'movie/index.html', context)


def movie_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    movie = Movie.objects.get(id=id)
    schedules = MovieSchedule.objects.all()
    schedules = schedules.filter(movie=movie, status=True)
    schedule_groups = MovieSchedule.group_by_date(schedules)
    context = {
        "movie": movie,
        "schedule_groups": schedule_groups,
        "WEEKDAY_MAP": MovieSchedule.WEEKDAY_MAP,
        "LANGUAGE_MAP": Movie.LANGUAGE_MAP,
        "GENRES_MAP": Movie.GENRES_MAP,
        "RATE_MAP": Movie.RATE_MAP,
    }
    return render(request, 'movie/detail.html', context)

def booking(request, auditorium, date, time):
    year = date // 10000
    month = date % 10000 // 100
    day = date % 100
    hour = time // 3600
    minute = time % 3600 // 60
    schedules = MovieSchedule.objects.all()

    auditorium = Auditorium.objects.get(id=auditorium)

    schedule = schedules.filter(
        auditorium = auditorium,
        date=datetime.datetime(year=year, month=month, day=day),
        time=datetime.time(hour=hour, minute=minute)
    ).first()

    rows = []
    for i in range(auditorium.rows):
        row = []
        for j in range(auditorium.seats_per_row):
            row.append({
                "id": i * auditorium.seats_per_row + j,
                "name": chr(ord("A") + i) + str(j+1),
                "status": schedule.seats_state[i * auditorium.seats_per_row + j],
            })
        rows.append(row)

    context = {
        "auditorium": auditorium,
        "schedule": schedule,
        "rows": rows,
    }
    return render(request, 'booking/seats.html', context)