#!/usr/bin/env python

from django.db import models

from bodzify_api import settings
from bodzify_api.model.base.PrivateStandardResource \
    import PrivateStandardResource, Fields as PrivateStandardResourceFields
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseManager \
    import MusicbrainzRecordingMissingCauseManager


class Fields:
    USER = PrivateStandardResourceFields.USER
    CREATED_ON = PrivateStandardResourceFields.CREATED_ON
    UPDATED_ON = PrivateStandardResourceFields.UPDATED_ON
    CODE = 'code'
    MESSAGE = 'message'


class MusicbrainzRecordingMissingCause(PrivateStandardResource):
    code = models.ForeignKey(MusicbrainzRecordingMissingCauseCode, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX, null=True)

    objects = MusicbrainzRecordingMissingCauseManager()

    class Meta:
        db_table = 'bodzify_api_musicbrainz_recording_missing_cause'
        verbose_name = 'MusicBrainz Recording Missing Cause'
        verbose_name_plural = 'MusicBrainz Recording Missing Causes'

    def __str__(self):
        return f"{self.user}: {self.code} - {self.message}"
