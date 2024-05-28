#!/usr/bin/env python

import shortuuid

from django.db import models

from bodzify_api import settings
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist


class MusicbrainzRecording(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    recording_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(MusicbrainzArtist, on_delete=models.CASCADE)
    duration = models.IntegerField()
    release_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'musicbrainz_recording'
        verbose_name = 'Musicbrainz Recording'
        verbose_name_plural = 'Musicbrainz Recordings'
