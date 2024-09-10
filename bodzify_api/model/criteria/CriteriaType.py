#!/usr/bin/env python

from django.db import models


class CRITERIA_TYPES_ID:
    GENRE = 0
    TAG = 1


class CRITERIA_TYPES_LABEL:
    GENRE = "genre"
    TAG = "tag"


class ATTRIBUTES_LABEL:
    LABEL = "label"


class CriteriaType(models.Model):
    label = models.CharField(unique=True, max_length=20)

    def __str__(self) -> str:
        return str(self.pk) + " " + self.label

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(label=""), name="criteria_non_empty_label")
        ]
        db_table = 'bodzify_api_criteria_type'
        verbose_name = 'Criteria Type'
        verbose_name_plural = 'Criteria Types'
