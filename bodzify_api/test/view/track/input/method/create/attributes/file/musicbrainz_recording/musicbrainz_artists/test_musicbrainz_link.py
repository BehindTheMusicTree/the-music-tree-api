from rest_framework import status
from django.db.models import QuerySet

from bodzify_api.model.musicbrainz_resource.children.artist.MusicbrainzArtist import MusicbrainzArtist
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_musicbrainz_link(self):
        response = self._post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording
        musicbrainz_artists: QuerySet[MusicbrainzArtist] = \
            self.saved_lib_track.track_file.musicbrainz_recording.musicbrainz_artists
        assert musicbrainz_artists[0].musicbrainz_link == (
            "https://musicbrainz.org/artist/0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        )
