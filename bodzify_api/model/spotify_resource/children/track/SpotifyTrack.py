import datetime
from django.db import models
from django.db.models import F, Value

from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.field.foreign_key.AppManyToManyField import AppManyToManyField
from bodzify_api.model.utils.ConcatOp import ConcatOp
from bodzify_api.model.spotify_resource.spotify_artist.SpotifyArtist import SpotifyArtist
from bodzify_api.model.spotify_resource.spotify_resource.SpotifyResource import SpotifyResource
from bodzify_api.model.spotify_resource.children.track.Fields import Fields
from bodzify_api.model.spotify_resource.children.track.SpotifyTrackManager import SpotifyTrackManager


class SpotifyTrack(SpotifyResource):
    """Represents a track from Spotify in the user's library."""

    name = AppCharField(max_length=256, editable=False, db_column=Fields.NAME)
    duration_ms = models.IntegerField(editable=False, db_column=Fields.DURATION_MS)
    popularity = models.IntegerField(null=True, editable=False, db_column=Fields.POPULARITY)
    spotify_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value("https://open.spotify.com/track/"), F(Fields.SPOTIFY_ID)),
        output_field=AppCharField(max_length=500),
        db_persist=True,
        db_column=Fields.SPOTIFY_LINK
    )
    album = models.JSONField(null=True, editable=False, db_column=Fields.ALBUM)
    preview_url = models.URLField(null=True, blank=True, editable=False, max_length=512, db_column=Fields.PREVIEW_URL)
    explicit = models.BooleanField(default=False, editable=False, db_column=Fields.EXPLICIT)
    spotify_artists = AppManyToManyField(SpotifyArtist, db_column=Fields.SPOTIFY_ARTISTS)
    last_synced_at = models.DateTimeField(null=True, editable=False, db_column=Fields.LAST_SYNCED_AT)
    is_removed = models.BooleanField(
        default=False,
        editable=False,
        help_text="Indicates if the track has been removed from Spotify",
        db_column=Fields.IS_REMOVED
    )

    objects = SpotifyTrackManager()

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        return str(datetime.timedelta(milliseconds=self.duration_ms))

    def __str__(self):
        return f"{self.name} ({self.duration_str_in_hour_min_sec})"

    def format_duration(self) -> str:
        """Format the duration in milliseconds to a human-readable string."""
        seconds = self.duration_ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

    class Meta:
        verbose_name = 'Spotify Track'
        verbose_name_plural = 'Spotify Tracks'
        indexes = [models.Index(fields=[Fields.SPOTIFY_ID], name='sp_track_id_idx')]
        db_table = 'spotify_track'
