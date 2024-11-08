from django.db import models


class TrackablePlayCount(models.Model):
    play_count = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
