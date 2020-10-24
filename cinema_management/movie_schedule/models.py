from enum import unique
from django.db import models
from movie.models import Movie
from auditorium.models import Auditorium

# Create your models here.
class MovieSchedule(models.Model):
    id         = models.AutoField(primary_key=True)
    movie      = models.ForeignKey(Movie, related_name='movie_schedule', on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, related_name='auditorium', on_delete=models.CASCADE)

    class Meta:
        verbose_name        = "Lịch chiếu"
        verbose_name_plural = "Lịch chiếu"
        unique_together     = ('auditorium', 'movie',)