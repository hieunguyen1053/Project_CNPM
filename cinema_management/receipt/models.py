from combo.models import Combo
from django.db import models
from django.urls import reverse
from member.models import Member
from movie_schedule.models import MovieSchedule
from staff.models import Staff


# Create your models here.
class Receipt(models.Model):
    id      = models.AutoField(primary_key=True)
    member  = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    staff   = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    date    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Biên lai"
        verbose_name_plural = "Biên lai"

    def serialize(self):
        tickets = Ticket.objects.filter(receipt=self)
        combos = ComboDetail.objects.filter(receipt=self)

        if len(tickets) != 0:
            movie = tickets[0].schedule.movie
            auditorium = tickets[0].schedule.auditorium

            tickets = [ticket.serialize() for ticket in tickets]
            combos = [combo.serialize() for combo in combos]


            return {
                "id": self.id,
                "movie": movie.serialize(),
                "member": self.member.serialize(),
                "staff": self.staff.serialize(),
                "date": self.date,
                "auditorium": auditorium.serialize(),
                "tickets": tickets,
                "combos": combos,
                "tickets_price": self.get_tickets_price(),
                "combos_price": self.get_combos_price(),
                "price": self.get_tickets_price() + self.get_combos_price(),
            }
        else:
            combos = [combo.serialize() for combo in combos]

            return {
                "id": self.id,
                "movie": "",
                "member": self.member.serialize(),
                "staff": self.staff.serialize(),
                "date": self.date,
                "auditorium": "",
                "tickets": "",
                "combos": combos,
                "tickets_price": "",
                "combos_price": self.get_combos_price(),
                "price": self.get_combos_price(),
            }

    def get_tickets_price(self):
        tickets = Ticket.objects.filter(receipt=self)
        tickets_price = tickets[0].schedule.price * len(tickets)
        return tickets_price


    def get_combos_price(self):
        combos = ComboDetail.objects.filter(receipt=self)
        combos_price = sum([combo.combo.price * combo.amount for combo in combos])
        return combos_price


    # def get_absolute_url(self):
    #     return reverse('movie-detail', args=[str(self.id)])

class ComboDetail(models.Model):
    id      = models.AutoField(primary_key=True)
    combo   = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True)
    amount  = models.IntegerField()
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "combo"  : self.combo.serialize(),
            "amount" : self.amount,
        }

# Create your models here.
class Ticket(models.Model):
    id        = models.AutoField(primary_key=True)
    schedule  = models.ForeignKey(MovieSchedule, on_delete=models.SET_NULL, null=True)
    member    = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    seat      = models.PositiveIntegerField()
    receipt   = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    class Meta:
        verbose_name        = "Vé"
        verbose_name_plural = "Vé"
        unique_together = (("schedule", "seat"))

    def serialize(self):
        return {
            "id"       : self.id,
            "schedule" : self.schedule.serialize(),
            "member"   : self.member.serialize(),
            "seat"     : self.get_seat(),
        }

    def get_seat(self):
        auditorium = self.schedule.auditorium
        seats_per_row = auditorium.seats_per_row

        row = self.seat // seats_per_row
        col = self.seat % seats_per_row

        row = chr(row + ord('A'))
        return row + str(col)
