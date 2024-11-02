from django.db import models


class Fields:
    PLAY_COUNT = 'play_count'


class TrackablePlayCountModel(models.Model):
    play_count = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
