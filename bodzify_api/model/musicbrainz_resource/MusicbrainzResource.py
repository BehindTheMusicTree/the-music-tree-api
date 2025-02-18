
from bodzify_api import settings
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.field.AppCharField import AppCharField


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = AppCharField(max_length=settings.MUSICBRAINZ_ID_LEN_MAX, unique=True)

    class Meta:
        abstract = True
