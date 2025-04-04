
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_0_then_0(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 0})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 0

    def test_1_then_13(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 1})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 13

    def test_1_then_1(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 2})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 1

    def test_3_then_54(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 3})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 54

    def test_4_then_64(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 4})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 64

    def test_5_then_118(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 5})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 118

    def test_6_then_128(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 6})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 128

    def test_7_then_186(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 7})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 186

    def test_8_then_196(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 8})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 196

    def test_9_then_242(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 9})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 242

    def test_10_then_255(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255
