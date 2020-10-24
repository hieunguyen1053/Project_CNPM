from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Movie


def all(request):
    if request.method == "GET":
        try:
            movies = Movie.objects.all()
            paginator = Paginator(movies, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            paginator = {
                "number": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
            }
            movies = [movie.serialize() for movie in page_obj]
            return JsonResponse({"movies": movies, "paginator": paginator})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        try:
            Movie.objects.create(
                title = request.POST.get("title"),
                director = request.POST.get("director"),
                actor = request.POST.get("actor"),
                description = request.POST.get("description"),
                genres = Movie.generate_genres(request.POST.get("genre")),
                release_date = request.POST.get("release_date"),
                time = request.POST.get("time"),
                language = request.POST.get("language"),
                rate = request.POST.get("rate"),
            )
            return JsonResponse({"message": "Đã thêm phim thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(id=id)
            schedules = movie.get_schedule()
            movie = movie.serialize()
            return JsonResponse({"movie": movie, "schedules": schedules})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            movie = Movie.objects.get(id=id)
            movie.title = request.POST.get("title")
            movie.director = request.POST.get("director")
            movie.actor = request.POST.get("actor")
            movie.description = request.POST.get("description")
            movie.genres = Movie.generate_genres(request.POST.get("genre"))
            movie.release_date = request.POST.get("release_date")
            movie.time = request.POST.get("time")
            movie.language = request.POST.get("language")
            movie.rate = request.POST.get("rate")
            movie.status = True if request.POST.get("status") == "true" else False
            movie.save()
            return JsonResponse({"message": "Đã chỉnh sửa phim thành công."})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def delete(request, id):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return JsonResponse({"message": "Đã xoá phim thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})
