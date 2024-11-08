from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.BaseModel import BaseModel


class FingerprintMissingCauseCode(BaseModel):
    class Codes(models.IntegerChoices):
        AUDIO_META_AMALYSIS_DISABLED = 0
        SERVICE_NOT_FOUND = 1
        FPCALC_ERROR_WITH_STATUS_2 = 2
        WRONG_FILE_EXTENSION = 3
        WRONG_FILE_TYPE = 4
        FILE_NOT_FOUND_IN_POOL = 5
        UNKNOWN_BAD_REQUEST = 6
        INTERNAL_ERROR = 7
        TIMEOUT_ERROR = 8
        UNKNOWN_CONNEXION_ERROR = 9
        UNKNOWN_UNPROCESSABLE_ENTITY_ERROR = 10

    code = models.IntegerField(primary_key=True, choices=Codes.choices, unique=True)
    label = models.CharField(unique=True, max_length=settings.FINGERPRINTING_ERROR_CODE_LABEL_LEN_MAX)

    def __str__(self) -> str:
        return f"{self.pk} {self.label}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(label=""), name="fingerprint_missing_cause_non_empty_label")]
        verbose_name = 'Fingerprinting Error Code'
        verbose_name_plural = 'Fingerprinting Error Codes'
