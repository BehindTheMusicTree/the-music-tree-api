import pytest
from rest_framework import status

from api.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_musicbrainz_link(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_WEARETHECHAMPIONS_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        musicbrainz_artists: list[MbArtist] = \
            list(self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all())
        assert musicbrainz_artists[0].musicbrainz_link == (
            "https://musicbrainz.org/artist/0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        )
