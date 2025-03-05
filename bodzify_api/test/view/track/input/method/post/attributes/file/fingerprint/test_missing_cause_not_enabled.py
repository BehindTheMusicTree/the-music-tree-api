import logging

import docker.errors
from rest_framework import status

from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode
)
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s    %(name)s:%(filename)s:%(lineno)d %(message)s')


class TestCase(LibTrackTestCase):

    def test_audio_meta_analysis_not_enabled_then_corresponding_missing_cause(self):
        response = self._post_lib_track(TestLibTrackFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file
        assert self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code == \
            FingerprintMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED
