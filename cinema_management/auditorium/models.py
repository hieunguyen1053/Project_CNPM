from django.db import models

# Create your models here.
class Auditorium(models.Model):
    class Type(models.IntegerChoices):
        NORMAL     = 0  #Rạp 2D
        IMAX       = 1  #IMAX
        LAMOUR     = 2  #LAMOUR
        STARIUM    = 3  #STARIUM
        GOLD       = 4  #GOLD CLASS
        PREMIUM    = 5  #PREMIUM
        CINELIVING = 6  #Cine & Living Room
        CINESUITE  = 7  #Cine & Living Room

    id     = models.AutoField(primary_key=True)
    type   = models.IntegerField(choices=Type.choices)
    rows   = models.IntegerField(default=5)
    seats  = models.IntegerField(default=10)

    class Meta:
        verbose_name        = "Rạp chiếu"
        verbose_name_plural = "Rạp chiếu"