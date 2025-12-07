import pytest
from unittest.mock import patch
from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_musicbrainz_link(self):
        with patch('acoustid.lookup') as mock_lookup:
            mock_lookup.return_value = {
                'status': 'ok',
                'results': [
                    {
                        'score': 1.0,
                        'recordings': [
                            {
                                'id': '2f880dca-3a46-42c4-a0a0-ecdba619d2d1',
                                'title': 'We Are the Champions',
                                'artists': [
                                    {
                                        'id': '0383dadf-2a4e-4d10-a46a-e9e041da8eb3',
                                        'name': 'Queen'
                                    }
                                ],
                                'duration': 181
                            }
                        ]
                    }
                ]
            }
            response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_DANS_LA_LEGENDE_FLAC)
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording
            assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_link == (
                "https://musicbrainz.org/recording/2f880dca-3a46-42c4-a0a0-ecdba619d2d1"
            )
