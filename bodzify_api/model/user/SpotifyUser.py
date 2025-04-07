from django.db import models

from bodzify_api.model.user.User import User


class SpotifyUser(User):
    spotify_id = models.CharField(max_length=255, unique=True)
    spotify_access_token = models.TextField(null=True, blank=True)
    spotify_refresh_token = models.TextField(null=True, blank=True)
    spotify_profile = models.JSONField(null=True, blank=True)
    spotify_token_expires_at = models.DateTimeField(null=True, blank=True)
    spotify_library_last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of when the user's Spotify library was last synced"
    )
    spotify_sync_in_progress = models.BooleanField(
        default=False,
        help_text="Indicates if a Spotify library sync is currently in progress"
    )

    def __str__(self):
        return f"{self.username} (Spotify)"

    class Meta:
        verbose_name = 'Spotify User'
        verbose_name_plural = 'Spotify Users'
