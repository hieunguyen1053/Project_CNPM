from django.db import models
from django.urls import reverse


# Create your models here.
class Movie(models.Model):
    LANGUAGE_MAP = {
        0: "Tiếng Việt",
        1: "Tiếng Anh - phụ đề Tiếng Việt"
    }

    GENRES_MAP = {
        1:   "Hành động",   #ACTION
        2:   "Phiêu lưu",   #ADVENTURE
        4:   "Hoạt hình",   #ANIMATION
        8:   "Hài",         #COMEDY
        16:  "Tội phạm",    #CRIME
        32:  "Tâm lý",      #DRAMA
        64:  "Gia đình",    #FAMILY
        128: "Kinh dị",     #HORROR
        256: "Hồi hộp",     #THRILLER
    }

    RATE_MAP = {
        0: "P",
        1: "C13",
        2: "C16",
        3: "C18"
    }

    """ Binary mask
    Genre
    - ACTION    = 1
    - ADVENTURE = 2
    - ANIMATION = 4
    - COMEDY    = 8
    - CRIME     = 16
    - DRAMA     = 32
    - FAMILY    = 64
    - HORROR    = 128
    - THRILLER  = 256
    """
    class Rating(models.IntegerChoices):
        P   = 0
        C13 = 1
        C16 = 2
        C18 = 3

    class Language(models.IntegerChoices):
        VI        = 0
        ENG_VISUB = 1

    id           = models.AutoField(primary_key=True)
    title        = models.CharField(max_length=50)
    director     = models.CharField(max_length=50)
    actor        = models.TextField(max_length=150)
    description  = models.TextField()
    release_date = models.DateField()
    image_url    = models.URLField(null=True)
    time         = models.PositiveIntegerField()
    genres       = models.PositiveIntegerField(default=0)
    language     = models.PositiveIntegerField(choices=Language.choices)
    rate         = models.PositiveIntegerField(choices=Rating.choices)
    status       = models.BooleanField(default=True)

    class Meta:
        verbose_name        = "Phim"
        verbose_name_plural = "Phim"

    def serialize(self):
        return {
            "id"           : self.id,
            "title"        : self.title,
            "director"     : self.director,
            "actor"        : self.actor,
            "description"  : self.description,
            "release_date" : self.release_date,
            "time"         : self.time,
            "genre"        : self.get_genres(),
            "image_url"    : self.image_url,
            "language"     : self.language,
            "rate"         : self.rate,
            "status"       : self.status,
            # "url"          : self.get_absolute_url(),
        }

    @classmethod
    def generate_genres(cls, genres):
        genres = [genre.strip() for genre in genres.split(",")]
        GENRES_MAP = {v: k for k, v in cls.GENRES_MAP.items()}
        genres = {GENRES_MAP[genre] for genre in genres}
        return sum(genres)

    def get_genres(self):
        binary = bin(self.genres)[-1:1:-1]
        return ", ".join([self.GENRES_MAP[2**i] for (i, x) in enumerate(binary) if x == "1"])

    def get_language(self):
        return self.LANGUAGE_MAP[self.language]

    def get_rate(self):
        return self.RATE_MAP[self.rate]

    def get_schedule(self):
        from movie_schedule.models import MovieSchedule
        schedules = MovieSchedule.objects.all()
        schedules = [schedule.serialize() for schedule in schedules]

        date = {}
        for schedule in schedules:
            if schedule["date"] in date:
                date[schedule["date"].__str__()].append(schedule)
            else:
                date[schedule["date"].__str__()] = [schedule]
        return date

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id)])
