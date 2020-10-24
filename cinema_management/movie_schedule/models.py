from enum import unique
from django.db import models
from movie.models import Movie
from auditorium.models import Auditorium

# Create your models here.
class MovieSchedule(models.Model):
    id         = models.AutoField(primary_key=True)
    movie      = models.ForeignKey(Movie, related_name='movie_schedule', on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, related_name='auditorium_schedule', on_delete=models.CASCADE)
    date       = models.DateField()
    time       = models.TimeField()
    price      = models.PositiveIntegerField()
    status     = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Lịch chiếu"
        verbose_name_plural = "Lịch chiếu"
        unique_together     = ('auditorium', 'date', 'time')

    def serialize(self):
        return {
            "id"         : self.id,
            "movie"      : self.movie.serialize(),
            "auditorium" : self.auditorium.serialize(),
            "date"       : self.date,
            "time"       : self.time,
            "price"      : self.price,
            "status"     : self.status,
            # "url"          : self.get_absolute_url(),
        }