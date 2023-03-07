#!/usr/bin/env python
from django.db import models


class CriteriaTypesIds:
    GENRE = 0
    TAG = 1


class CriteriaType(models.Model):
    label = models.CharField(unique=True, max_length=20, default=None)

    def __str__(self) -> str:
        return str(self.id) + " " + self.label
