import logging

from rest_framework import status

from bodzify_api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode
)
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s    %(name)s:%(filename)s:%(lineno)d %(message)s')


class TestCase(UploadedTrackTestCase):

    def test_audio_meta_analysis_not_enabled_then_corresponding_missing_cause(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file
        assert self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code == \
            FingerprintMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED
