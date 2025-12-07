
from api import settings
from api.model.field.AppCharField import AppCharField
from api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = AppCharField(max_length=settings.MB_ID_LEN_MAX, unique=True)

    class Meta:
        abstract = True
