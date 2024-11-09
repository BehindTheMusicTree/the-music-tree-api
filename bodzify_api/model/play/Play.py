from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from .Fields import Fields


class Play(PrivateStandardResource):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(Fields.CONTENT_TYPE, Fields.OBJECT_PK)

    class Meta:
        verbose_name = 'Play'
        verbose_name_plural = 'Plays'
        indexes = [models.Index(fields=[Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_PK]),]
