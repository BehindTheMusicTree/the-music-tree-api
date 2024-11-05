from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateUniqueResource import PrivateUniqueResource
from .code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from .FingerprintMissingCauseManager import FingerprintMissingCauseManager


class FingerprintMissingCause(PrivateUniqueResource):

    code = models.ForeignKey(FingerprintMissingCauseCode, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=settings.FINGERPRINTING_ERROR_MESSAGE_LEN_MAX, null=True)

    objects = FingerprintMissingCauseManager()

    def __str__(self) -> str:
        return f"{self.code} | {self.message}"

    class Meta:
        db_table = f'{settings.APP_NAME}_fingerprint_missing_cause'
        verbose_name = 'Fingerprinting Error'
        verbose_name_plural = 'Fingerprinting Errors'
