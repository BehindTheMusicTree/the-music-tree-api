import pytest
from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_drown_7m21_mp3_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Drown (Massano remix)"

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_5M35_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        if self.saved_object.track_file.musicbrainz_recording_missing_cause:
            print(self.saved_object.track_file.musicbrainz_recording_missing_cause)
            assert False

        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Total Eclipse of the Heart"

    def test_upload_same_track_twice_then_title_updated(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        recording1 = self.saved_object.track_file.musicbrainz_recording
        assert recording1
        assert recording1.title == "Drown (Massano remix)"

        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        recording2 = self.saved_object.track_file.musicbrainz_recording
        assert recording2
        assert recording2.musicbrainz_id == recording1.musicbrainz_id
        assert recording2.title == "Drown (Massano remix)"
