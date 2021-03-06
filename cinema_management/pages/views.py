import datetime
import json

from auditorium.models import Auditorium
from combo.models import Combo
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from member.models import Member
from movie.models import Movie
from movie_schedule.models import MovieSchedule
from receipt.models import ComboDetail, Receipt, Ticket
from staff.models import Staff


# Create your views here
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    context = {
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'admin/receipt.html', context)

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
    return render(request, 'admin/movie.html', context)

def admin_auditorium(request):
    if not request.user.is_superuser:
        return redirect('login')
    context = {
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'admin/auditorium.html', context)

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
    return render(request, 'admin/schedule.html', context)

def admin_member(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin/member.html')

def admin_staff(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin/staff.html')

def admin_combo(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin/combo.html')

def admin_receipt(request):
    if not request.user.is_superuser:
        return redirect('login')
    context = {
        "TYPE_MAP": Auditorium.TYPE_MAP,
    }
    return render(request, 'admin/receipt.html', context)

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
    return render(request, 'staff/movie-list.html', context)


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
    return render(request, 'staff/movie-detail.html', context)

def booking_seats(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    schedule = MovieSchedule.objects.get(id=id)
    rows = schedule.get_seats()
    context = {
        "schedule": schedule,
        "rows": rows,
    }
    return render(request, 'staff/book-seat.html', context)

def booking_combos(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        if request.POST.get("seats") != "":
            seats = request.POST.get("seats")
            seats = json.loads(seats)
            schedule = MovieSchedule.objects.get(id=id)
            combos = Combo.objects.all()
            combos = [combo.serialize() for combo in combos]
            context = {
                "schedule": schedule,
                "seats": seats,
                "combos": combos,
            }
            return render(request, 'staff/book-combo.html', context)
        return redirect(booking_seats, id)

def booking_check(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        if request.POST.get("seats") != "":
            seats = request.POST.get("seats")
            seats = json.loads(seats)
            combos = request.POST.get("combos")
            combos = json.loads(combos)
            schedule = MovieSchedule.objects.get(id=id)
            context = {
                "schedule": schedule,
                "seats": seats,
                "combos": combos,
            }
            return render(request, 'staff/book-check.html', context)
        return redirect(booking_seats, id)

def add_member(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'staff/add-member.html')

def combo_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    combos = Combo.objects.all()
    combos = [combo.serialize() for combo in combos]
    context = {
        "combos": combos,
    }
    return render(request, 'staff/combo-list.html', context)

def combo_check(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        combos = request.POST.get("combos")
        combos = json.loads(combos)
        context = {
            "combos": combos,
        }
        return render(request, 'staff/combo-check.html', context)
    return redirect('combo_list')