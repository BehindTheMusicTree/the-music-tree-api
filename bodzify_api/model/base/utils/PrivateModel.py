#!/usr/bin/env python

from django.db import models

from bodzify_api import settings


class Fields:
    USER = 'user'


class PrivateModel(models.Model):
    user = models.ForeignKey(f'{settings.APP_NAME}.User', on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True
