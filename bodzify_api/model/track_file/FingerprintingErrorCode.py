#!/usr/bin/env python

from django.db import models


class ATTRIBUTES_LABEL:
    LABEL = "label"


class FINGERPRINTING_ERROR_CODES:
    SERVICE_NOT_FOUND = 0
    FPCALC_ERROR_WITH_STATUS_2 = 1
    WRONG_FILE_EXTENSION = 2
    WRONG_FILE_TYPE = 3
    FILE_NOT_FOUND_IN_POOL = 4
    UNKNOWN_BAD_REQUEST = 5
    INTERNAL_ERROR = 6
    TIMEOUT_ERROR = 7
    UNKNOWN_CONNEXION_ERROR = 8
    UNKNOWN_UNPROCESSABLE_ENTITY_ERROR = 9


class FingerprintingErrorCode(models.Model):
    label = models.CharField(unique=True, max_length=200)

    def __str__(self) -> str:
        return str(self.pk) + " " + self.label

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(label=""),
                                   name="fingerprinting_error_code_non_empty_label")
        ]
        db_table = 'bodzify_api_fingerprinting_error_code'
        verbose_name = 'Fingerprinting Error Code'
        verbose_name_plural = 'Fingerprinting Error Codes'
