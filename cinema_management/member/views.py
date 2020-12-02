from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Member


def all(request):
    if request.method == "GET":
        try:
            members = Member.objects.all()
            paginator = Paginator(members, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            paginator = {
                "number": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
            }
            members = [member.serialize() for member in members]
            return JsonResponse({"members": members, "paginator": paginator})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def create(request):
    if request.method == "POST":
        try:
            Member.objects.create(
                id = Member.generate_id(),
                secret = Member.generate_secret(),
                full_name = request.POST.get("full_name"),
                id_card = request.POST.get("id_card"),
                birthday = request.POST.get("birthday"),
                is_vip = True if request.POST.get("is_vip") == "true" else False,
            )
            return JsonResponse({"message": "Đã thêm thẻ thành viên thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def get(request, id):
    if request.method == "GET":
        try:
            member = Member.objects.get(id=id)
            member = member.serialize()
            return JsonResponse({"member": member})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def edit(request, id):
    if request.method == "POST":
        try:
            member = Member.objects.get(id=id)
            member.full_name = request.POST.get("full_name")
            member.id_card = request.POST.get("id_card")
            member.birthday = request.POST.get("birthday")
            member.is_vip = True if request.POST.get("is_vip") == "true" else False
            member.save()
            return JsonResponse({"message": "Đã chỉnh sửa thẻ thành công thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def delete(request, id):
    if request.method == "GET":
        try:
            member = Member.objects.get(id=id)
            member.delete()
            return JsonResponse({"message": "Đã xoá lịch chiếu thành công."})
        except Exception as e:
            return JsonResponse({"error": "Đã có lỗi xảy ra."})

def verify(request):
    if request.method == "POST":
        member = request.POST.get("member")
        secret = request.POST.get("secret")
        if len(Member.objects.filter(id=member, secret=secret)) != 0:
            return JsonResponse({"message": "Xác nhận thành công."})
        else:
            return JsonResponse({"message": "Hội viên không tồn tại"})