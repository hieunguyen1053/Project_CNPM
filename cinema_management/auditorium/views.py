from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Auditorium


def all(request):
    if request.method == "GET":
        try:
            auditoriums = Auditorium.objects.all()
            paginator = Paginator(auditoriums, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            paginator = {
                "number": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
            }
            auditoriums = [auditorium.serialize() for auditorium in auditoriums]
            auditoriums = sorted(auditoriums, key=lambda auditorium: auditorium["name"])
            return JsonResponse({"auditoriums": auditoriums, "paginator": paginator})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        try:
            num_seats = int(request.POST.get("rows")) * int(request.POST.get("seats_per_row"))
            print(num_seats)
            Auditorium.objects.create(
                name = request.POST.get("name"),
                type = request.POST.get("type"),
                rows = request.POST.get("rows"),
                seats_per_row = int(request.POST.get("seats_per_row")),
                seats_state = "0" * num_seats,
            )
            return JsonResponse({"message": "Đã thêm rạp chiếu thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            auditorium = Auditorium.objects.get(id=id)
            auditorium = auditorium.serialize()
            return JsonResponse({"auditorium": auditorium})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            auditorium = Auditorium.objects.get(id=id)
            auditorium.name = request.POST.get("name")
            auditorium.type = request.POST.get("type")
            auditorium.rows = request.POST.get("rows")
            auditorium.seats_per_row = request.POST.get("seats_per_row")
            auditorium.seats_state = request.POST.get("seats_state")
            auditorium.save()
            return JsonResponse({"message": "Đã chỉnh sửa rạp thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def delete(request, id):
    if request.method == "GET":
        try:
            auditorium = Auditorium.objects.get(id=id)
            auditorium.delete()
            return JsonResponse({"message": "Đã xoá rạp thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})
