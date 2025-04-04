
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields


class TestCase(LibTrackTestCase):

    def test_none_then_none(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_0_then_0(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 0})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 0

    def test_1_then_10(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 1})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 10

    def test_2_then_20(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 2})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 20

    def test_3_then_30(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 3})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 30

    def test_4_then_40(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 4})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 40

    def test_5_then_50(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 5})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 50

    def test_6_then_60(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 6})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 60

    def test_7_then_70(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 7})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 70

    def test_8_then_80(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 8})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 80

    def test_9_then_90(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 9})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 90

    def test_10_then_100(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100
