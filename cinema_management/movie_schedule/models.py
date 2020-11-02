from enum import unique
from django.db import models
from movie.models import Movie
from auditorium.models import Auditorium

# Create your models here.
class MovieSchedule(models.Model):
    WEEKDAY_MAP = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }

    id          = models.AutoField(primary_key=True)
    movie       = models.ForeignKey(Movie, related_name='movie_schedule', on_delete=models.CASCADE)
    auditorium  = models.ForeignKey(Auditorium, related_name='auditorium_schedule', on_delete=models.CASCADE)
    date        = models.DateField()
    time        = models.TimeField()
    seats_state = models.TextField()
    price       = models.PositiveIntegerField()
    status      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Lịch chiếu"
        verbose_name_plural = "Lịch chiếu"
        unique_together     = ('auditorium', 'date', 'time')

    def serialize(self):
        return {
            "id"          : self.id,
            "movie"       : self.movie.serialize(),
            "auditorium"  : self.auditorium.serialize(),
            "date"        : self.date,
            "time"        : self.time,
            "seats_state" : self.seats_state,
            "price"       : self.price,
            "status"      : self.status,
            # "url"          : self.get_absolute_url(),
        }

    @classmethod
    def group_by_date(cls, schedules):
        schedule_groups = {}
        for schedule in schedules:
            if schedule.date not in schedule_groups:
                schedule_groups[schedule.date] = [schedule]
            else:
                schedule_groups[schedule.date].append(schedule)

        for schedule_group in schedule_groups.values():
            schedule_group.sort(key=lambda schedule: schedule.time)
        return schedule_groups

    def get_time(self):
        return self.time.strftime("%I:%M %p")

    def get_time_url(self):
        t = self.time
        return t.hour * 3600 + t.minute * 60

    def get_date_url(self):
        return self.date.strftime("%Y%m%d")