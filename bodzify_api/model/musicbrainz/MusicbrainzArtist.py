#!/usr/bin/env python

from django.utils import timezone
from django.db import models


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    NAME = 'name'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class MusicbrainzArtist(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, default=None)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'musicbrainz_artist'
        verbose_name = 'MusicBrainz Artist'
        verbose_name_plural = 'MusicBrainz Artists'
