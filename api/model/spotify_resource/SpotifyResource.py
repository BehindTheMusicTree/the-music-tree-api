from api.model.field.AppCharField import AppCharField
from api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class SpotifyResource(PublicStandardResource):
    spotify_id = AppCharField(max_length=50, unique=True, null=False, blank=False, primary_key=True)

    class Meta:
        abstract = True
