from auditorium.models import Auditorium
from django.db.utils import IntegrityError
from django.http import JsonResponse
from movie.models import Movie

from .models import MovieSchedule


def all(request):
    if request.method == "GET":
        try:
            schedules = MovieSchedule.objects.all()
            schedules = [schedule.serialize() for schedule in schedules]
            return JsonResponse({"schedules": schedules})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        print(request.POST)
        try:
            movie = request.POST.get("movie")
            movie = Movie.objects.get(id=movie)
            auditorium = request.POST.get("auditorium")
            auditorium = Auditorium.objects.get(id=auditorium)
            listtime = request.POST.getlist("time")
            for time in listtime:
                MovieSchedule.objects.create(
                    movie = movie,
                    auditorium = auditorium,
                    time = time,
                    date = request.POST.get("date"),
                    price = request.POST.get("price"),
                )
            return JsonResponse({"message": "Đã thêm lịch chiếu thành công."})
        except IntegrityError as e:
            return JsonResponse({"error": "Rạp chiếu đã tồn tại lịch chiếu"})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            schedule = MovieSchedule.objects.get(id=id)
            schedule = schedule.serialize()
            return JsonResponse({"schedule": schedule})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            movie = request.POST.get("movie")
            movie = Movie.objects.get(id=movie)
            auditorium = request.POST.get("auditorium")
            auditorium = Auditorium.objects.get(id=auditorium)

            schedule = MovieSchedule.objects.get(id=id)
            schedule.movie = movie
            schedule.auditorium = auditorium
            schedule.date = request.POST.get("date")
            schedule.time = request.POST.get("time")
            schedule.price = request.POST.get("price")
            schedule.save()
            return JsonResponse({"message": "Đã chỉnh sửa lịch chiếu thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def delete(request, id):
    if request.method == "GET":
        try:
            movie = MovieSchedule.objects.get(id=id)
            movie.delete()
            return JsonResponse({"message": "Đã xoá phim thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})
