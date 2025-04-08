from django.db import models
from django.db.models import F, Value
from django.contrib.postgres.fields import ArrayField

from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.utils.ConcatOp import ConcatOp
from bodzify_api.model.spotify.SpotifyResource import SpotifyResource
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from .Fields import Fields
from .SpotifyArtistManager import SpotifyArtistManager


class SpotifyArtist(SpotifyResource, PublicStandardResource):
    name = AppCharField(max_length=256, editable=False)
    popularity = models.IntegerField(null=True, editable=False)
    spotify_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value("https://open.spotify.com/artist/"), F(Fields.SPOTIFY_ID)),
        output_field=AppCharField(max_length=500),
        db_persist=True)
    genres = ArrayField(models.CharField(max_length=100), null=True, editable=False)
    images = models.JSONField(null=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    objects = SpotifyArtistManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Spotify Artist'
        verbose_name_plural = 'Spotify Artists'
        indexes = [models.Index(fields=[Fields.SPOTIFY_ID], name='sp_artist_id_idx')]
