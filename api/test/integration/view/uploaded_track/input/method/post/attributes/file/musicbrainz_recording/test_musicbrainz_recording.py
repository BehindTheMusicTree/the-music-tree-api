
import pytest
from unittest.mock import patch
from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_no_matching_recording_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_TOKYO_DRIFT_NO_MB_RECORDING_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.track_file.musicbrainz_recording

    def test_with_9_matches_then_the_one_with_duration_field(self):
        with patch('acoustid.lookup') as mock_lookup:
            mock_lookup.return_value = {
                'status': 'ok',
                'results': [
                    {
                        'score': 1.0,
                        'recordings': [
                            {
                                'id': '9f3c3b61-41a6-4bb9-a49c-33606f536784',
                                'title': 'Total Eclipse of the Heart',
                                'artists': [
                                    {
                                        'id': '35abc6e5-01e7-4c4b-8281-868503be3bce',
                                        'name': 'Bonnie Tyler'
                                    }
                                ],
                                'duration': 281
                            }
                        ]
                    }
                ]
            }
            response = self._post_uploaded_track(
                UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_9_MATCHES_BUT_ONE_WITH_DURATION_FLAC)

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording
            assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_id == \
                '9f3c3b61-41a6-4bb9-a49c-33606f536784'

    def test_with_2_matches_then_the_one_with_closest_duration(self):
        with patch('acoustid.lookup') as mock_lookup:
            mock_lookup.return_value = {
                'status': 'ok',
                'results': [
                    {
                        'score': 1.0,
                        'recordings': [
                            {
                                'id': '76e1d5e6-9713-4c6b-8238-9d7983fd4497',
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
            response = self._post_uploaded_track(
                UploadedTrackTestFilename.RECORDING_LORIE_2_MATCHES_BUT_ONE_WITH_CLOSEST_DURATION_MP3)

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording
            assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_id == \
                '76e1d5e6-9713-4c6b-8238-9d7983fd4497'

    def test_with_2_matches_with_same_duration_and_same_number_of_fields_then_the_one_with_the_most_release_groups(self):
        with patch('acoustid.lookup') as mock_lookup:
            mock_lookup.return_value = {
                'status': 'ok',
                'results': [
                    {
                        'score': 1.0,
                        'recordings': [
                            {
                                'id': '82b4c5fe-0980-4495-95b0-bd5e124486d8',
                                'title': 'Allumer le feu',
                                'artists': [
                                    {
                                        'id': 'e9980382-32f0-4a7d-b8c0-c12d5d86fbd5',
                                        'name': 'Johnny Hallyday'
                                    }
                                ],
                                'duration': 181
                            }
                        ]
                    }
                ]
            }
            response = self._post_uploaded_track(
                UploadedTrackTestFilename.RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3)

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording
            assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_id == \
                '82b4c5fe-0980-4495-95b0-bd5e124486d8'

    def test_with_25_matches_then_select_the_one_with_closest_duration_and_most_fields_and_most_release_groups(self):
        # TODO: Implement this test as musicbrainz changes the recording id
        # response = self._post_uploaded_track(
        #     TestUploadedTrackFilename.RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3)
        # assert response.status_code == status.HTTP_201_CREATED
        # assert self.saved_object.track_file.musicbrainz_recording
        # assert self.saved_object.track_file.musicbrainz_recording.musicbrainz_id == \
        #     '3604eb06-4bc2-4416-9b31-ceadae51bc70'
        pass
