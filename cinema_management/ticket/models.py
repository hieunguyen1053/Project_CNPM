from django.db import models
from movie_schedule.models import MovieSchedule
from member.models import Member

# Create your models here.
class Ticket(models.Model):
    id        = models.AutoField(primary_key=True)
    schedule  = models.ForeignKey(MovieSchedule, on_delete=models.SET_NULL, null=True)
    member    = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    seat      = models.PositiveIntegerField()

    class Meta:
        verbose_name        = "Vé"
        verbose_name_plural = "Vé"

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
