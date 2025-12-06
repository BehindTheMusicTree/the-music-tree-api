import pytest
import warnings

from django.db.models import QuerySet
from rest_framework import status

from bodzify_api.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_one_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_WEARETHECHAMPIONS_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        musicbrainz_artists: QuerySet[MbArtist] = \
            self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
        assert musicbrainz_artists[0].musicbrainz_id == "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        assert musicbrainz_artists[0].name == "Queen"

    def test_multiple_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        if self.saved_object.track_file.musicbrainz_recording:
            musicbrainz_artists: QuerySet[MbArtist] = \
                self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
            artists_musicbrainz_ids = [artist.musicbrainz_id for artist in musicbrainz_artists]
            assert "d2fe3873-d123-4bea-a5ee-4340d865777c" in artists_musicbrainz_ids
            assert "c4d2d3d2-8c93-499e-9c9e-571bf0d5cf29" in artists_musicbrainz_ids

            artists_musicbrainz_names = [artist.name for artist in musicbrainz_artists]
            assert "Juan Hansen" in artists_musicbrainz_names
            assert "Øostil" in artists_musicbrainz_names
        else:
            warnings.warn("Musicbrainz recording not found for test_multiple_then_ok")

    def test_same_artist_then_same_uuid(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_WEARETHECHAMPIONS_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        musicbrainz_artists: QuerySet[MbArtist] = \
            self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
        first_track_musicbrainz_artist_id = musicbrainz_artists[0].musicbrainz_id

        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_WEARETHECHAMPIONS_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        musicbrainz_artists: QuerySet[MbArtist] = \
            self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
        second_track_musicbrainz_artist_id = musicbrainz_artists[0].musicbrainz_id

        assert first_track_musicbrainz_artist_id == second_track_musicbrainz_artist_id
