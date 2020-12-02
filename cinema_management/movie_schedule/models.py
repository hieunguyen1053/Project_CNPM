from enum import unique
from django.db import models
from movie.models import Movie
from auditorium.models import Auditorium

# Create your models here.
class Seat:
    def __init__(self, id=None, name=None, status=0):
        self.id = id
        self.name = name
        self.status = status

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
                schedule_groups[schedule.date] = []
            schedule_groups[schedule.date].append(schedule)

        for group in schedule_groups:
            schedule_groups[group] = cls.group_by_auditorium(schedule_groups[group])
        print(schedule_groups)
        return schedule_groups

    @classmethod
    def group_by_auditorium(cls, schedules):
        schedule_groups = {}
        for schedule in schedules:
            if schedule.auditorium not in schedule_groups:
                schedule_groups[schedule.auditorium] = []
            schedule_groups[schedule.auditorium].append(schedule)
        return schedule_groups

    def get_time(self):
        return self.time.strftime("%I:%M %p")

    def get_seats(self):
        num_rows = self.auditorium.rows
        num_cols = self.auditorium.seats_per_row

        rows = []
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                seat = Seat(
                    id = i * num_cols + j,
                    name = chr(ord("A") + i) + str(j+1),
                    status = self.seats_state[i * num_cols + j]
                )
                row.append(seat)
            rows.append(row)
        return rows