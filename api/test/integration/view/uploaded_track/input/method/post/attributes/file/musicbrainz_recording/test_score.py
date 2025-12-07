import pytest
from unittest.mock import patch
from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    @patch('acoustid.lookup')
    def test_totaleclipse_with_three_scores_then_highest(self, mock_lookup):
        mock_lookup.return_value = {
            'status': 'ok',
            'results': [{
                'score': 0.95,
                'recordings': [{
                    'id': '9f3c3b61-41a6-4bb9-a49c-33606f536784',
                    'title': 'Total Eclipse of the Heart',
                    'artists': [{'id': '0383dadf-2a4e-4d10-a46a-e9e041da8eb3', 'name': 'Bonnie Tyler'}],
                    'duration': 281
                }]
            }, {
                'score': 0.99,
                'recordings': [{
                    'id': '9f3c3b61-41a6-4bb9-a49c-33606f536785',
                    'title': 'Total Eclipse of the Heart',
                    'artists': [{'id': '0383dadf-2a4e-4d10-a46a-e9e041da8eb3', 'name': 'Bonnie Tyler'}],
                    'duration': 281
                }]
            }, {
                'score': 0.97,
                'recordings': [{
                    'id': '9f3c3b61-41a6-4bb9-a49c-33606f536786',
                    'title': 'Total Eclipse of the Heart',
                    'artists': [{'id': '0383dadf-2a4e-4d10-a46a-e9e041da8eb3', 'name': 'Bonnie Tyler'}],
                    'duration': 281
                }]
            }]
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        assert musicbrainz_recording
        assert float(musicbrainz_recording.score) > 0.98
