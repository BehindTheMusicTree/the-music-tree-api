from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class SpotifyResource(PublicStandardResource):
    spotify_id = AppCharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        abstract = True
