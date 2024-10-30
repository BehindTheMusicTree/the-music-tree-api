#!/usr/bin/env python

from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResourceManager \
    import PublicStandardResourceManager


class MusicbrainzRecordingMissingCauseManager(PublicStandardResourceManager):

    def create(self, *args, **kwargs):
        from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause import Fields
        from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
            import MusicbrainzRecordingMissingCauseCode

        code = kwargs.pop(Fields.CODE, None)
        if code is None:
            raise ValueError("The code parameter must be provided when creating an entry.")

        musicbrainz_recording_missing_cause_code = MusicbrainzRecordingMissingCauseCode.objects.get(code=code)
        kwargs[Fields.CODE] = musicbrainz_recording_missing_cause_code

        return super().create(*args, **kwargs)
