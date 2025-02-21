import pytest
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_musicbrainz_link(self):
        response = self._post_lib_track_with_specific_sample("queen_duration_181.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_link == (
            "https://musicbrainz.org/recording/3604eb06-4bc2-4416-9b31-ceadae51bc70"
        )
