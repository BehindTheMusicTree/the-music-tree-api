#!/usr/bin/env python

import uuid

from django.db import models

from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel


class Fields:
    UUID = 'uuid'


class UuidModel(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
