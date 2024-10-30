#!/usr/bin/env python

from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.function.ConcatOp import ConcatOp
from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResource import PublicStandardResource, Fields as PublicStandardResourceFields


class Fields:
    CREATED_ON = PublicStandardResourceFields.CREATED_ON
    UPDATED_ON = PublicStandardResourceFields.UPDATED_ON
    MUSICBRAINZ_ID = 'musicbrainz_id'
    MUSICBRAINZ_LINK = 'musicbrainz_link'


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = models.CharField(max_length=settings.MUSICBRAINZ_ID_LEN_MAX, unique=True)
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MUSICBRAINZ_RECORDING_URL), F(Fields.MUSICBRAINZ_ID)),
        output_field=models.CharField(max_length=len(settings.MUSICBRAINZ_RECORDING_URL) + settings.UUID_LEN),
        db_persist=True)

    class Meta:
        abstract = True
