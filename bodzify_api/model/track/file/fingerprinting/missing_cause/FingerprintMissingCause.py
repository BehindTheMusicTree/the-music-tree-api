from django.db import models

from bodzify_api import settings
from bodzify_api.model.private_unique_resource.PrivateUniqueResource import PrivateUniqueResource
from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.field.AppCharField import AppCharField
from .code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from .FingerprintMissingCauseManager import FingerprintMissingCauseManager


class FingerprintMissingCause(PrivateUniqueResource):

    code = AppForeignKey(FingerprintMissingCauseCode, on_delete=models.DO_NOTHING)
    message = AppCharField(max_length=settings.FINGERPRINTING_ERROR_MESSAGE_LEN_MAX, null=True)

    objects = FingerprintMissingCauseManager()

    def __str__(self) -> str:
        return f"{self.code} | {self.message}"

    class Meta:
        verbose_name = 'Fingerprinting Error'
        verbose_name_plural = 'Fingerprinting Errors'
