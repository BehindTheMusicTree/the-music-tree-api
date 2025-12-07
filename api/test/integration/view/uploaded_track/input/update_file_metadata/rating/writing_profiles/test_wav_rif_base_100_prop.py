
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields


class TestCase(UploadedTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_rating_then_expected(self):
        test_cases = [
            (0, 0),
            (1, 13),
            (2, 1),
            (3, 54),
            (4, 64),
            (5, 118),
            (6, 128),
            (7, 186),
            (8, 196),
            (9, 242),
            (10, 255),
        ]
        for input_rating, expected in test_cases:
            with self.subTest(input_rating=input_rating, expected=expected):
                response = self._post_uploaded_track(
                    UploadedTrackTestFilename.METADATA_NONE_WAV, **{PostFields.RATING: input_rating})
                assert response.status_code == 201
                assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == expected
