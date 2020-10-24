from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Staff(User):
    class Meta:
        proxy = True
        verbose_name        = "Nhân viên"
        verbose_name_plural = "Nhân viên"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
        }