from django.db import models

from api import settings
from api.model.base.BaseModel import BaseModel
from api.model.field.AppCharField import AppCharField


class MbRecordingMissingCauseCode(BaseModel):
    class Codes(models.IntegerChoices):
        AUDIO_META_AMALYSIS_DISABLED = 0
        DURATION_BELOW_OR_EQUAL_1_SEC = 1
        LOOKUP_FOUND_NO_MATCHING_RECORDING = 2
        LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT = 3
        LOOKUP_FAILED_WITH_INTERNAL_ERROR = 4
        LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE = 5
        LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE = 6
        LOOKUP_FAILED_DNS_RESOLUTION_ERROR = 7

    code = models.PositiveIntegerField(primary_key=True, choices=Codes.choices, unique=True)
    label = AppCharField(unique=True, max_length=settings.MB_RECORDING_MISSING_CAUSE_CODE_LABEL_LEN_MAX)

    class Meta:
        verbose_name = 'MusicBrainz Recording Missing Cause Code'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes Codes'
