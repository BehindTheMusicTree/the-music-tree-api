
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields


class TestCase(UploadedTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_rating_then_expected(self):
        test_cases = [
            (0, 0),
            (1, 10),
            (2, 20),
            (3, 30),
            (4, 40),
            (5, 50),
            (6, 60),
            (7, 70),
            (8, 80),
            (9, 90),
            (10, 100),
        ]
        for input_rating, expected in test_cases:
            with self.subTest(input_rating=input_rating, expected=expected):
                response = self._post_uploaded_track(
                    UploadedTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: input_rating})
                assert response.status_code == 201
                assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == expected
