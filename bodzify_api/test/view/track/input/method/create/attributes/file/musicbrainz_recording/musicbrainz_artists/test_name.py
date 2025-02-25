import pytest
from django.db.models import QuerySet
from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_one_then_ok(self):
        response = self._post_lib_track_with_specific_sample("queen_wearethechampions.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        artists: QuerySet[Artist] = self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
        assert artists[0].name == "Queen"

    def test_multiple_then_ok(self):
        response = self._post_lib_track_with_specific_sample("oostil_Juan Hansen.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        artists: QuerySet[Artist] = self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
        artists_names = [artist.name for artist in artists]
        assert "Øostil" in artists_names
        assert "Juan Hansen" in artists_names
