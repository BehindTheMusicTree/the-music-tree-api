from django.db import models

class Song (models.Model):

    name = models.CharField("name", max_length=150, unique=False)
    author = models.CharField("author", max_length=150, unique=False)

    class Meta:
        verbose_name = "song"
        verbose_name_plural = "songs"

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)