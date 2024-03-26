#!/usr/bin/env python

import shortuuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    USER = 'user'
    CONTENT_TYPE = 'content_type'
    OBJECT_ID = 'object_id'
    CONTENT_OBJECT = 'content_object'
    TIME = 'time'


class Play(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=22)
    content_object = GenericForeignKey('content_type', 'object_id')
    time = models.DateTimeField(auto_now_add=True)
