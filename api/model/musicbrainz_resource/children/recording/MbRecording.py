import datetime

from django.db import models
from django.db.models import F, Value

from api import settings
from api.model.field.AppCharField import AppCharField
from api.model.field.foreign_key.AppManyToManyField import AppManyToManyField
from api.model.utils.ConcatOp import ConcatOp

from ...MusicbrainzResource import MusicbrainzResource
from ..artist.MbArtist import MbArtist
from .Fields import Fields


class MusicbrainzRecording(MusicbrainzResource):
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MB_RECORDING_URL), F(Fields.MUSICBRAINZ_ID)),
        output_field=AppCharField(max_length=len(settings.MB_RECORDING_URL) + settings.UUID_LEN),
        db_persist=True)
    title = AppCharField(max_length=settings.MB_RECORDING_TITLE_LEN_MAX, editable=False)
    score = models.DecimalField(max_digits=9, decimal_places=8, editable=False)
    duration_in_sec = models.IntegerField(editable=False, null=True)
    release_date = models.DateField(null=True, blank=True, editable=False)
    musicbrainz_artists = AppManyToManyField(MbArtist)

    @property
    def duration_str_in_hour_min_sec(self) -> str | None:
        return str(datetime.timedelta(seconds=self.duration_in_sec)) if self.duration_in_sec else None

    def __str__(self):
        return f"{self.title} - {self.musicbrainz_artists} ({self.duration_str_in_hour_min_sec})"

    class Meta:
        verbose_name = 'MusicBrainz Recording'
        verbose_name_plural = 'MusicBrainz Recordings'
        indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name='mb_recording_id_idx')]
