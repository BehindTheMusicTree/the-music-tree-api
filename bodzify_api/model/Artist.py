#!/usr/bin/env python

import shortuuid

from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
        primary_key=True,
        default=shortuuid.uuid,
        max_length=22,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default=None, blank=True, null=True)
