#!/usr/bin/env python

import shortuuid

from django.db import models

from bodzify_api import settings


class MusicbrainzArtist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    artist_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'musicbrainz_artist'
        verbose_name = 'MusicBrainz Artist'
        verbose_name_plural = 'MusicBrainz Artists'
