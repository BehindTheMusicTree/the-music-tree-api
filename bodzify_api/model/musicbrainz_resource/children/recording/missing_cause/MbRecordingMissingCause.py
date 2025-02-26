from django.db import models

from bodzify_api import settings
from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource

from .code.MbRecordingMissingCauseCode import MbRecordingMissingCauseCode
from .MbRecordingMissingCauseManager import MbRecordingMissingCauseManager


class MbRecordingMissingCause(PrivateStandardResource):
    code: MbRecordingMissingCauseCode = AppForeignKey(  # type: ignore
        MbRecordingMissingCauseCode, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX, null=True)

    objects: MbRecordingMissingCauseManager = MbRecordingMissingCauseManager()

    class Meta:
        verbose_name = 'MusicBrainz Recording Missing Cause'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes'

    def __str__(self):
        return f"{self.user}: {self.code} - {self.message}"
