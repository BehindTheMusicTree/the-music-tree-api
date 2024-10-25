#!/usr/bin/env python

from django.db import models

from bodzify_api import settings


class Fields:
    CODE = 'code'
    LABEL = 'label'


class MusicbrainzRecordingMissingCauseCode(models.Model):
    class Codes(models.IntegerChoices):
        AUDIO_META_AMALYSIS_DISABLED = 0
        TRACK_FILE_MISSING = 1
        TRACK_FILE_FINGERPRINTING_FAILED = 2
        DURATION_BELOW_1_SEC = 3
        LOOKUP_FOUND_NO_MATCHING_RECORDING = 4
        LOOKUP_FAILED_WITH_RESPONSE_ERROR_CODE = 5
        LOOKUP_FAILED_WITH_RESPONSE_UNKNOWN_STATUS_CODE = 6
        LOOKUP_FAILED_FOR_UNKNOWN_REASON = 7

    code = models.PositiveIntegerField(primary_key=True, choices=Codes.choices, unique=True)
    label = models.CharField(unique=True, max_length=settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX)

    class Meta:
        db_table = 'bodzify_api_musicbrainz_recording_missing_cause_code'
        verbose_name = 'MusicBrainz Recording Missing Cause Code'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes Codes'
