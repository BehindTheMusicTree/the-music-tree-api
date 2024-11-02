
from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateUniqueResource \
    import PrivateUniqueResource, Fields as PrivateStandardResourceFields
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCauseCode \
    import FingerprintMissingCauseCode
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCauseManager \
    import FingerprintMissingCauseManager


class Fields:
    CREATED_ON = PrivateStandardResourceFields.CREATED_ON
    UPDATED_ON = PrivateStandardResourceFields.UPDATED_ON
    USER = PrivateStandardResourceFields.USER
    UUID = PrivateStandardResourceFields.UUID
    CODE = "code"
    MESSAGE = "message"


class FingerprintMissingCause(PrivateUniqueResource):

    code = models.ForeignKey(FingerprintMissingCauseCode, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=settings.FINGERPRINTING_ERROR_MESSAGE_LEN_MAX, null=True)

    objects = FingerprintMissingCauseManager()

    def __str__(self) -> str:
        return f"{self.code} {self.message}"

    class Meta:
        db_table = f'{settings.APP_NAME}_fingerprint_missing_cause'
        verbose_name = 'Fingerprinting Error'
        verbose_name_plural = 'Fingerprinting Errors'
