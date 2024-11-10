from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.utils.ConcatOp import ConcatOp
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from .Fields import Fields


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = models.CharField(max_length=settings.MUSICBRAINZ_ID_LEN_MAX, unique=True)

    class Meta:
        abstract = True
