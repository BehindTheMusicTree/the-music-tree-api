from django.db import models

from bodzify_api import settings
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from .MusicbrainzRecordingMissingCauseManager import MusicbrainzRecordingMissingCauseManager
from .code.MusicbrainzRecordingMissingCauseCode import MusicbrainzRecordingMissingCauseCode


class MusicbrainzRecordingMissingCause(PrivateStandardResource):
    code = AppForeignKey(MusicbrainzRecordingMissingCauseCode, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX, null=True)

    objects: MusicbrainzRecordingMissingCauseManager = MusicbrainzRecordingMissingCauseManager()

    class Meta:
        verbose_name = 'MusicBrainz Recording Missing Cause'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes'

    def __str__(self):
        return f"{self.user}: {self.code} - {self.message}"
