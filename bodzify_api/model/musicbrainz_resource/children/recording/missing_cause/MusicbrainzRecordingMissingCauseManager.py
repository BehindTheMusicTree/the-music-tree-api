from typing import Any
from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .Fields import Fields


class MusicbrainzRecordingMissingCauseManager(PublicStandardResourceManager):

    def create(self, *args, **kwargs):
        from .code.MusicbrainzRecordingMissingCauseCode import MusicbrainzRecordingMissingCauseCode

        code = kwargs.pop(Fields.CODE, None)
        if code is None:
            raise ValueError("The code parameter must be provided when creating an entry.")

        musicbrainz_recording_missing_cause_code = MusicbrainzRecordingMissingCauseCode.objects.get(code=code)
        kwargs[Fields.CODE] = musicbrainz_recording_missing_cause_code

        return super().create(*args, **kwargs)

    def delete_instance(self, instance: Any):
        raise NotImplementedError()
