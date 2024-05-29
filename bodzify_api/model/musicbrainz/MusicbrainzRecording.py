#!/usr/bin/env python

from django.utils import timezone
from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    TITLE = 'title'
    MUSICBRAINZ_ARTISTS = 'musicbrainz_artists'
    DURATION = 'duration'
    RELEASE_DATE = 'release_date'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class MusicbrainzRecording(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=settings.MUSICBRAINZ_RECORDING_TITLE_LEN_MAX)
    duration = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)
    musicbrainz_artists = models.ManyToManyField(MusicbrainzArtist)
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MUSICBRAINZ_RECORDING_URL), F(ATTRIBUTES_LABEL.UUID)),
        output_field=models.CharField(max_length=len(settings.MUSICBRAINZ_RECORDING_URL) + 36),
        db_persist=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'musicbrainz_recording'
        verbose_name = 'Musicbrainz Recording'
        verbose_name_plural = 'Musicbrainz Recordings'
