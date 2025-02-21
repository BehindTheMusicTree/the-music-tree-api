import pytest
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_duration_greater_to_one_sec_then_ok(self):
        response = self._post_lib_track_with_specific_sample("queen_duration_181.mp3")

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.duration_in_sec == 181

    def test_musicbrainz_recording_is_missing_duration_then_none(self):
        response = self._post_lib_track_with_specific_sample("Celinekin Park - no musicbrainz recording duration.mp3")

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert not self.saved_object.track_file.musicbrainz_recording.duration_in_sec
