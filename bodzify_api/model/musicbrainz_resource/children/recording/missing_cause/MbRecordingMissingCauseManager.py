from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .Fields import Fields


class MbRecordingMissingCauseManager(StandardResourceManager):

    def create(self, *args, **kwargs):
        from .code.MbRecordingMissingCauseCode import MbRecordingMissingCauseCode

        code = kwargs.pop(Fields.CODE, None)
        if code is None:
            raise ValueError("The code parameter must be provided when creating an entry.")

        musicbrainz_recording_missing_cause_code = MbRecordingMissingCauseCode.objects.get(code=code)
        kwargs[Fields.CODE] = musicbrainz_recording_missing_cause_code

        return super().create(*args, **kwargs)
