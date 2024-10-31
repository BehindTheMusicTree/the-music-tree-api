
import datetime
from typing import Optional

from django.db import models

from bodzify_api import settings
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.model.musicbrainz.MusicbrainzResource import MusicbrainzResource, Fields as MusicbrainzResourceFields


class Fields:
    CREATED_ON = MusicbrainzResourceFields.CREATED_ON
    UPDATED_ON = MusicbrainzResourceFields.UPDATED_ON
    MUSICBRAINZ_ID = MusicbrainzResourceFields.MUSICBRAINZ_ID
    MUSICBRAINZ_LINK = MusicbrainzResourceFields.MUSICBRAINZ_LINK
    TITLE = 'title'
    SCORE = 'score'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = "duration_str_in_hour_min_sec"
    RELEASE_DATE = 'release_date'
    MUSICBRAINZ_ARTISTS = 'musicbrainz_artists'
    MUSICBRAINZ_LINK = 'musicbrainz_link'


class MusicbrainzRecording(MusicbrainzResource):
    title = models.CharField(max_length=settings.MUSICBRAINZ_RECORDING_TITLE_LEN_MAX, editable=False)
    score = models.DecimalField(max_digits=9, decimal_places=8, editable=False)
    duration_in_sec = models.IntegerField(editable=False, null=True)
    release_date = models.DateField(null=True, blank=True, editable=False)
    musicbrainz_artists = models.ManyToManyField(MusicbrainzArtist)

    @property
    def duration_str_in_hour_min_sec(self) -> Optional[str]:
        return str(datetime.timedelta(seconds=self.duration_in_sec)) if self.duration_in_sec else None

    def __str__(self):
        return f"{self.title} - {self.musicbrainz_artists} ({self.duration_str_in_hour_min_sec})"

    class Meta:
        db_table = 'bodzify_api_musicbrainz_recording'
        verbose_name = 'MusicBrainz Recording'
        verbose_name_plural = 'MusicBrainz Recordings'
        indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name='mb_recording_id_idx')]
