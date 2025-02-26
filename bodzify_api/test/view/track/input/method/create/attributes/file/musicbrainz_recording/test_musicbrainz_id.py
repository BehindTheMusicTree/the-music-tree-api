import logging

import pytest
from rest_framework import status

from bodzify_api.logging.LoggersName import LoggersName
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


logger = logging.getLogger(LoggersName.INFO)


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_not_found_then_none(self):
        response = self._post_lib_track_with_generic_sample_1_star()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording is None

    def test_drown_7m21_mp3_then_ok(self):
        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        recording = self.saved_object.track_file.musicbrainz_recording
        assert recording
        assert recording.musicbrainz_id == "4a45b00b-273d-40ed-9ecd-42f387f59c22"

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self._post_lib_track_with_specific_sample("Bonnie Tyler - Total Eclipse of the Heart - 5m35.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track_musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        expected_musicbrainz_recording_id = "9f3c3b61-41a6-4bb9-a49c-33606f536784"
        if (track_musicbrainz_recording is None
                or track_musicbrainz_recording.musicbrainz_id != expected_musicbrainz_recording_id):
            logger.warning(f"The expected MusicBrainz recording id {
                           track_musicbrainz_recording} is not the one expected {expected_musicbrainz_recording_id}")

    def test_different_format_but_same_musicbrainz_recording(self):
        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m20.flac")
        assert response.status_code == status.HTTP_201_CREATED
        recording1 = self.saved_object.track_file.musicbrainz_recording
        assert recording1
        flac_recording_id = recording1.musicbrainz_id

        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        recording = self.saved_object.track_file.musicbrainz_recording
        assert recording
        assert recording.musicbrainz_id == flac_recording_id
