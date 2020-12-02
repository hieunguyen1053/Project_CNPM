import json

from combo.models import Combo
from django.http import JsonResponse
from member.models import Member
from movie.models import Movie
from movie_schedule.models import MovieSchedule
from staff.models import Staff

from receipt.models import ComboDetail, Receipt, Ticket


def create(request):
    if request.method == "POST":
        try:
            schedule = request.POST.get("schedule")
            schedule = MovieSchedule.objects.get(id=schedule)

            _staff = request.user.id
            staff = Staff.objects.get(id=_staff)

            _member = request.POST.get("member")
            member = Member.objects.get(id=_member)

            receipt = Receipt.objects.create(
                member = member,
                staff = staff,
            )

            _seats = request.POST.get("seats")
            _seats = json.loads(_seats)
            for _seat in _seats:
                ticket = Ticket.objects.create(
                    schedule = schedule,
                    member = member,
                    seat = _seat.get("id"),
                    receipt = receipt,
                )

            _combos = request.POST.get("combos")
            _combos = json.loads(_combos)
            for _combo in _combos:
                combo = Combo.objects.get(id=_combo.get("id"))
                combo_detail = ComboDetail.objects.create(
                    combo = combo,
                    amount = _combo.get("num"),
                    receipt = receipt,
                )

            tickets = Ticket.objects.filter(schedule = schedule)
            seats = [ticket.seat for ticket in tickets]
            seats_state = [seat for seat in schedule.seats_state]

            for seat_idx in seats:
                seats_state[seat_idx] = "1"
            schedule.seats_state = "".join(seats_state)
            schedule.save()

            return JsonResponse({"message": "Đã đặt thành công."})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Đã có lỗi xảy ra."})
