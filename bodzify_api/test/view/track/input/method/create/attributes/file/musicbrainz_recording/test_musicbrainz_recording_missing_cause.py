#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_ok_then_no_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()
        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_lib_track.track_file.musicbrainz_recording_missing_cause

    def test_no_matching_recording_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_specific_sample(
            "Tokyo Drift x Temperature - no musicbrainz recording.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING

    def test_duration_below_one_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_below_1_sec()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.DURATION_BELOW_1_SEC
