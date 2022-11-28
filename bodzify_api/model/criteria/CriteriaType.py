#!/usr/bin/env python

from django.db import models

class CriteriaTypesLabels:
    GENRE = 'genre'
    TAG = 'tag'

class CriteriaType(models.Model):
    label = models.CharField(unique=True, max_length=200, default=None, blank=False, null=False)

    def __str__(self) -> str:
        return str(self.id) + " " + self.label