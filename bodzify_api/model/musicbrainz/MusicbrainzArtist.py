#!/usr/bin/env python

from django.utils import timezone
from django.db import models
from django.db.models import Value, F

from bodzify_api import settings


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    NAME = 'name'
    MUSICBRAINZ_LINK = 'musicbrainz_link'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class MusicbrainzArtist(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=settings.MUSICBRAINZ_ARTIST_NAME_LEN_MAX, default=None)
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MUSICBRAINZ_ARTIST_URL), F(ATTRIBUTES_LABEL.UUID)),
        output_field=models.CharField(max_length=len(settings.MUSICBRAINZ_ARTIST_URL) + 36),
        db_persist=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bodzify_api_musicbrainz_artist'
        verbose_name = 'MusicBrainz Artist'
        verbose_name_plural = 'MusicBrainz Artists'
