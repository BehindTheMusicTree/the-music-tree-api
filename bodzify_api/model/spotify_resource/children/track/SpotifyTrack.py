import datetime

from django.db import models
from django.db.models import F, Value

from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.field.foreign_key.AppManyToManyField import AppManyToManyField
from bodzify_api.model.utils.ConcatOp import ConcatOp
from bodzify_api.model.spotify_resource.SpotifyResource import SpotifyResource
from bodzify_api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from .Fields import Fields


class SpotifyTrack(SpotifyResource):
    name = AppCharField(max_length=256, editable=False)
    duration_ms = models.IntegerField(editable=False)
    popularity = models.IntegerField(null=True, editable=False)
    spotify_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value("https://open.spotify.com/track/"), F(Fields.SPOTIFY_ID)),
        output_field=AppCharField(max_length=500),
        db_persist=True)
    album = models.JSONField(null=True, editable=False)
    preview_url = models.URLField(null=True, blank=True, editable=False, max_length=512)
    explicit = models.BooleanField(default=False, editable=False)
    spotify_artists = AppManyToManyField(SpotifyArtist)

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        return str(datetime.timedelta(milliseconds=self.duration_ms))

    def __str__(self):
        return f"{self.name} ({self.duration_str_in_hour_min_sec})"

    class Meta:
        verbose_name = 'Spotify Track'
        verbose_name_plural = 'Spotify Tracks'
        indexes = [models.Index(fields=[Fields.SPOTIFY_ID], name='sp_track_id_idx')]