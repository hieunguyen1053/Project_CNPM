from django.db import models
from django.urls import reverse

# Create your models here.
class Auditorium(models.Model):
    TYPE_MAP = {
        0: "Rạp 2D",
        1: "Rạp IMAX",
        2: "Rạp Lamour",
        3: "Rạp STARIUM",
        4: "Rạp GOLD CLASS",
        5: "Rạp PREMIUM",
        6: "Rạp Cine & Living Room",
        7: "Rạp Cine & Suite",
    }

    class Type(models.IntegerChoices):
        NORMAL     = 0  #Rạp 2D
        IMAX       = 1  #IMAX
        LAMOUR     = 2  #LAMOUR
        STARIUM    = 3  #STARIUM
        GOLD       = 4  #GOLD CLASS
        PREMIUM    = 5  #PREMIUM
        CINELIVING = 6  #Cine & Living Room
        CINESUITE  = 7  #Cine & Suite

    id             = models.AutoField(primary_key=True)
    name           = models.PositiveIntegerField(unique=True)
    type           = models.PositiveIntegerField(choices=Type.choices)
    rows           = models.PositiveIntegerField(default=5)
    seats_per_row  = models.PositiveIntegerField(default=10)

    class Meta:
        verbose_name        = "Rạp chiếu"
        verbose_name_plural = "Rạp chiếu"

    def serialize(self):
        return {
            "id"            : self.id,
            "name"          : self.name,
            "type"          : self.type,
            "rows"          : self.rows,
            "seats_per_row" : self.seats_per_row,
        }

    def get_type(self):
        return self.TYPE_MAP[self.type]

    def get_absolute_url(self):
        return reverse('auditorium-detail', args=[str(self.id)])