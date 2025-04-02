import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_musicbrainz_link(self):
        response = self._post_lib_track(LibTrackTestFilename.RECORDING_DANS_LA_LEGENDE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_link == (
            "https://musicbrainz.org/recording/2f880dca-3a46-42c4-a0a0-ecdba619d2d1"
        )
