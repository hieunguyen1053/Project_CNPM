from django.db import models

# Create your models here.
class Combo(models.Model):
    id        = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=50)
    image_url = models.URLField()
    price     = models.PositiveIntegerField()

    class Meta:
        verbose_name        = "Combo"
        verbose_name_plural = "Combo"

    def serialize(self):
        return {
            "id"        : self.id,
            "name"      : self.name,
            "image_url" : self.image_url,
            "price"     : self.price
        }