#!/usr/bin/env python

from datetime import timezone
import shortuuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from bodzify_api import settings


class AttributesLabels:
    UUID = 'uuid'
    USER = 'user'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'


class BaseModel(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True
