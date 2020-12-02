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
        return {
            "id": self.id,
            "member": self.member,
            "staff": self.staff,
            "date": self.date,
            "tickets": [],
            "combos": [],
        }

    # def get_absolute_url(self):
    #     return reverse('movie-detail', args=[str(self.id)])

class ComboDetail(models.Model):
    id      = models.AutoField(primary_key=True)
    combo   = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True)
    amount  = models.IntegerField()
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)


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
            "schedule" : self.schedule,
            "member"   : self.member,
            "seat"     : self.seat,
            # "url"          : self.get_absolute_url(),
        }

    def get_seat(self):
        auditorium = self.schedule.auditorium
        seats_per_row = auditorium.seats_per_row

        row = self.seat // seats_per_row
        col = self.seat % seats_per_row

        row = chr(row + ord('A'))
        return row + str(col)
