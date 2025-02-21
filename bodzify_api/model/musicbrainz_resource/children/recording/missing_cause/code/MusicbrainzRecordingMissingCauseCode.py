from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.model.field.AppCharField import AppCharField


class MusicbrainzRecordingMissingCauseCode(BaseModel):
    class Codes(models.IntegerChoices):
        AUDIO_META_AMALYSIS_DISABLED = 0
        TRACK_FILE_MISSING = 1
        TRACK_FILE_FINGERPRINTING_FAILED = 2
        DURATION_BELOW_OR_EQUAL_1_SEC = 3
        LOOKUP_FOUND_NO_MATCHING_RECORDING = 4
        LOOKUP_FAILED_WITH_INVALID_FINGERPRINT_RESPONSE_ERROR_CODE = 5
        LOOKUP_FAILED_WITH_INTERNAL_ERROR_RESPONSE_ERROR_CODE = 6
        LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE = 7
        LOOKUP_FAILED_WITH_RESPONSE_UNKNOWN_STATUS_CODE = 8
        LOOKUP_FAILED_DNS_RESOLUTION_ERROR = 9
        LOOKUP_FAILED_FOR_UNKNOWN_REASON = 10

    code = models.PositiveIntegerField(primary_key=True, choices=Codes.choices, unique=True)
    label = AppCharField(unique=True, max_length=settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX)

    class Meta:
        verbose_name = 'MusicBrainz Recording Missing Cause Code'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes Codes'
