#!/usr/bin/env python

import shortuuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api import settings


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    USER = 'user'
    CONTENT_TYPE = 'content_type'
    OBJECT_UUID = 'object_uuid'
    CONTENT_OBJECT = 'content_object'
    TIME = 'time'


class Play(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.CharField(max_length=settings.UUID_LEN)
    content_object = GenericForeignKey('content_type', 'object_uuid')
    time = models.DateTimeField(auto_now_add=True)
