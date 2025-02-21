import pytest
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_drown_7m21_mp3_then_ok(self):
        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Drown (Massano remix)"

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self._post_lib_track_with_specific_sample("Bonnie Tyler - Total Eclipse of the Heart - 5m35.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Total Eclipse of the Heart"
