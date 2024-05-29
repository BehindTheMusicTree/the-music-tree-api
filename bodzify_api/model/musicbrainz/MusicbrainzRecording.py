#!/usr/bin/env python

import datetime
from django.utils import timezone
from django.db import models
from django.db.models import F, Value
from django.db.models.expressions import Value

from bodzify_api import settings
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    TITLE = 'title'
    SCORE = 'score'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = "duration_str_in_hour_min_sec"
    RELEASE_DATE = 'release_date'
    MUSICBRAINZ_ARTISTS = 'musicbrainz_artists'
    MUSICBRAINZ_LINK = 'musicbrainz_link'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None  # type: ignore
    output_field = models.TextField()  # type: ignore
    template = "%(expressions)s"


class MusicbrainzRecording(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=settings.MUSICBRAINZ_RECORDING_TITLE_LEN_MAX, editable=False)
    score = models.DecimalField(max_digits=9, decimal_places=8, editable=False)
    duration_in_sec = models.IntegerField(editable=False)
    release_date = models.DateField(null=True, blank=True, editable=False)
    musicbrainz_artists = models.ManyToManyField(MusicbrainzArtist)
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MUSICBRAINZ_RECORDING_URL), F(ATTRIBUTES_LABEL.UUID)),
        output_field=models.CharField(max_length=len(settings.MUSICBRAINZ_RECORDING_URL) + 36),
        db_persist=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    @property
    def duration_str_in_hour_min_sec(self):
        return str(datetime.timedelta(seconds=self.duration_in_sec))

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'musicbrainz_recording'
        verbose_name = 'Musicbrainz Recording'
        verbose_name_plural = 'Musicbrainz Recordings'
