#!/usr/bin/env python

import uuid

from django.db import models

from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    TITLE = 'title'
    MUSICBRAINZ_ARTISTS = 'musicbrainz_artists'
    DURATION = 'duration'
    RELEASE_DATE = 'release_date'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class MusicbrainzRecording(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    musicbrainz_artists = models.ManyToManyField(MusicbrainzArtist)
    duration = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'musicbrainz_recording'
        verbose_name = 'Musicbrainz Recording'
        verbose_name_plural = 'Musicbrainz Recordings'
