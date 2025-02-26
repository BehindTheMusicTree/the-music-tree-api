
from rest_framework import status

from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


# Meta audio analysis is disabled by default for tests
class TestCase(LibTrackTestCase):
    def test_audio_meta_analysis_disabled_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED
