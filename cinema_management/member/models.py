from django.db import models

# Create your models here.
class Member(models.Model):
    id        = models.CharField(max_length=10, primary_key=True)
    secret    = models.CharField(max_length=3)
    full_name = models.CharField(max_length=50)
    id_card   = models.CharField(max_length=12)
    birthday  = models.DateField()
    is_vip    = models.BooleanField(default=False)


    class Meta:
        verbose_name        = "Hội viên"
        verbose_name_plural = "Hội viên"

    def serialize(self):
        return {
            "id"         : self.id,
            "full_name"  : self.full_name,
            "id_card"    : self.id_card,
            "birthday"   : self.birthday,
            "is_vip"     : self.is_vip,
            # "url"          : self.get_absolute_url(),
        }

    @classmethod
    def generate_id(cls):
        import random
        while True:
            id = "".join(str(random.randint(0,9)) for _ in range(10))
            if not cls.objects.filter(id=id).exists():
                return id

    @classmethod
    def generate_secret(cls):
        import random
        secret = "".join(str(random.randint(0,9)) for _ in range(3))
        return secret