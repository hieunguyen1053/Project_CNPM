from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Staff


def all(request):
    if request.method == "GET":
        try:
            staffs = Staff.objects.all()
            paginator = Paginator(staffs, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            paginator = {
                "number": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
            }
            staffs = [staff.serialize() for staff in staffs]
            return JsonResponse({"staffs": staffs, "paginator": paginator})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        try:
            Staff.objects.create_user(
                first_name = request.POST.get("first_name"),
                last_name = request.POST.get("last_name"),
                username = request.POST.get("username"),
                password = request.POST.get("password"),
                is_staff = True
            )
            return JsonResponse({"message": "Đã thêm nhân viên thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            staff = Staff.objects.get(id=id)
            staff = staff.serialize()
            return JsonResponse({"staff": staff})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            staff = Staff.objects.get(id=id)
            staff.username = request.POST.get("username")
            staff.first_name = request.POST.get("first_name")
            staff.last_name = request.POST.get("last_name")
            staff.is_superuser = True if request.POST.get("is_superuser") == "true" else False
            if request.POST.get("password"):
                staff.set_password(request.POST.get("password"))
            staff.save()
            return JsonResponse({"message": "Đã chỉnh sửa nhân viên thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def delete(request, id):
    if request.method == "GET":
        try:
            staff = Staff.objects.get(id=id)
            staff.delete()
            return JsonResponse({"message": "Đã xoá nhân viên thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})
