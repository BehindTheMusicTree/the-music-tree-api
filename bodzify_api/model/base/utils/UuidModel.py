#!/usr/bin/env python

import uuid

from django.db import models


class Fields:
    UUID = 'uuid'


class UuidModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
