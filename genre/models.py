from django.db import models

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def genres_list(cls):
        return list(cls.objects.values_list("title", flat=True))