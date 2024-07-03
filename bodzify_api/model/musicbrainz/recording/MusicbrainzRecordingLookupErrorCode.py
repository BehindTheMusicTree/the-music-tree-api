#!/usr/bin/env python

from django.db import models


class ATTRIBUTES_LABEL:
    LABEL = "label"


class MusicbrainzRecordingLookupErrorCode(models.Model):
    label = models.CharField(unique=True, max_length=200)

    def __str__(self) -> str:
        return str(self.pk) + " " + self.label

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(label=""),
                                   name="musicbrainz_recording_lookup_error_code_non_empty_label")
        ]
        db_table = 'bodzify_api_musicbrainz_recording_lookup_error_code'
        verbose_name = 'Musicbrainz Recording Lookup Error Code'
        verbose_name_plural = 'Musicbrainz Recording Lookup Error Codes'
