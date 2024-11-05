from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateStandardResource import PrivateStandardResource
from .Fields import Fields


class Play(PrivateStandardResource):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_uuid')

    class Meta:
        db_table = f'{settings.APP_NAME}_play'
        verbose_name = 'Play'
        verbose_name_plural = 'Plays'
        indexes = [models.Index(fields=[Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_PK]),]
