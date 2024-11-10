from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.utils.ConcatOp import ConcatOp
from ...MusicbrainzResource import MusicbrainzResource
from .Fields import Fields


class MusicbrainzArtist(MusicbrainzResource):
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MUSICBRAINZ_ARTIST_URL), F(Fields.MUSICBRAINZ_ID)),
        output_field=models.CharField(max_length=len(settings.MUSICBRAINZ_RECORDING_URL) + settings.UUID_LEN),
        db_persist=True)
    name = models.CharField(max_length=settings.MUSICBRAINZ_ARTIST_NAME_LEN_MAX, default=None)

    def __str__(self):
        return f"{self.musicbrainz_id} | {self.name}"

    class Meta:
        verbose_name = 'Musicbrainz Artist'
        verbose_name_plural = 'Musicbrainz Artists'
        indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name='mb_artist_id_idx')]
