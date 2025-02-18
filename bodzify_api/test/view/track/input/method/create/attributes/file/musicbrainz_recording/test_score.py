from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_totaleclipse_with_three_scores_then_highest(self):
        response = self._post_lib_track_with_specific_sample("total_eclipse_3_scores.flac")
        assert response.status_code == status.HTTP_201_CREATED
        musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        assert musicbrainz_recording
        assert float(musicbrainz_recording.score) > 0.98
