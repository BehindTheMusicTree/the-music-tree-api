#!/usr/bin/env python

from re import M
from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.musicbrainz.MusicbrainzResource import MusicbrainzResource, Fields as MusicbrainzResourceFields


class Fields:
    CREATED_ON = MusicbrainzResourceFields.CREATED_ON
    UPDATED_ON = MusicbrainzResourceFields.UPDATED_ON
    MUSICBRAINZ_ID = MusicbrainzResourceFields.MUSICBRAINZ_ID
    MUSICBRAINZ_LINK = MusicbrainzResourceFields.MUSICBRAINZ_LINK
    NAME = 'name'


class MusicbrainzArtist(MusicbrainzResource):
    name = models.CharField(max_length=settings.MUSICBRAINZ_ARTIST_NAME_LEN_MAX, default=None)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bodzify_api_musicbrainz_artist'
        verbose_name = 'Musicbrainz Artist'
        verbose_name_plural = 'Musicbrainz Artists'
        indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name='mb_artist_id_idx')]
