from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
from .models import Combo

def all(request):
    if request.method == "GET":
        try:
            combos = Combo.objects.all()
            paginator = Paginator(combos, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            paginator = {
                "number": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
            }
            combos = [combo.serialize() for combo in page_obj]
            return JsonResponse({"combos": combos, "paginator": paginator})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        try:
            Combo.objects.create(
                name = request.POST.get("name"),
                price = request.POST.get("price"),
                image_url = request.POST.get("image_url"),
            )
            return JsonResponse({"message": "Đã thêm combo thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            combo = Combo.objects.get(id=id)
            combo = combo.serialize()
            return JsonResponse({"combo": combo})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            combo = Combo.objects.get(id=id)
            combo.name = request.POST.get("name")
            combo.price = request.POST.get("price")
            combo.image_url = request.POST.get("image_url")
            combo.save()
            return JsonResponse({"message": "Đã chỉnh sửa combo thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})


def delete(request, id):
    if request.method == "GET":
        try:
            combo = Combo.objects.get(id=id)
            combo.delete()
            return JsonResponse({"message": "Đã xoá phim thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})