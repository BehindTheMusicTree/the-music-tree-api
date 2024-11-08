from django.db import models

from bodzify_api import settings
from bodzify_api.model.musicbrainz_resource.MusicbrainzResource import MusicbrainzResource
from .Fields import Fields


class MusicbrainzArtist(MusicbrainzResource):
    name = models.CharField(max_length=settings.MUSICBRAINZ_ARTIST_NAME_LEN_MAX, default=None)

    def __str__(self):
        return f"{self.musicbrainz_id} | {self.name}"

    # class Meta:
    #     verbose_name = 'Musicbrainz Artist'
    #     verbose_name_plural = 'Musicbrainz Artists'
    #     indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name='mb_artist_id_idx')]
