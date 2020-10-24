from django.http import JsonResponse
from .models import Movie

def __convert(genres):
    genres = [genre.strip() for genre in genres.split(",")]
    GENRES_MAP = {v: k for k, v in Movie.GENRES_MAP.items()}
    genres = {GENRES_MAP[genre] for genre in genres}
    return sum(genres)

def all(request):
    if request.method == "GET":
        try:
            movies = Movie.objects.all()
            movies = [movie.serialize() for movie in movies]
            return JsonResponse({"movies": movies})
        except Exception as e:
            return JsonResponse({"error": e})

def create(request):
    if request.method == "POST":
        try:
            Movie.objects.create(
                title = request.POST.get("title"),
                director = request.POST.get("director"),
                actor = request.POST.get("actor"),
                description = request.POST.get("description"),
                genres = __convert(request.POST.get("genre")),
                release_date = request.POST.get("release_date"),
                time = int(request.POST.get("time")),
                language = request.POST.get("language"),
                rate = request.POST.get("rate"),
            )
            return JsonResponse({"message": "Đã thêm phim thành công."})
        except Exception as e:
            return JsonResponse({"error": e})

def get(request, id):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(id=id)
            movie = movie.serialize()
            return JsonResponse({"movie": movie})
        except Exception as e:
            return JsonResponse({"error": e})

def edit(request, id):
    if request.method == "POST":
        try:
            movie = Movie.objects.get(id=id)
            movie.title = request.POST.get("title")
            movie.director = request.POST.get("director")
            movie.actor = request.POST.get("actor")
            movie.description = request.POST.get("description")
            movie.genres = __convert(request.POST.get("genre"))
            movie.release_date = request.POST.get("release_date")
            movie.time = int(request.POST.get("time"))
            movie.language = request.POST.get("language")
            movie.rate = request.POST.get("rate")
            movie.save()
            return JsonResponse({"message": "Đã chỉnh sửa phim thành công."})
        except Exception as e:
            return JsonResponse({"error": e})

def delete(request, id):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return JsonResponse({"message": "Đã xoá phim thành công."})
        except Exception as e:
            return JsonResponse({"error": e})
