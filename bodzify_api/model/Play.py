
import shortuuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateStandardResource \
    import PrivateStandardResource, Fields as PrivateStandardResourceFields


class Fields:
    CREATED_ON = PrivateStandardResourceFields.CREATED_ON
    UPDATED_ON = PrivateStandardResourceFields.UPDATED_ON
    USER = PrivateStandardResourceFields.USER
    CONTENT_TYPE = 'content_type'
    OBJECT_UUID = 'object_uuid'
    CONTENT_OBJECT = 'content_object'
    TIME = 'time'


class Play(PrivateStandardResource):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_uuid')
