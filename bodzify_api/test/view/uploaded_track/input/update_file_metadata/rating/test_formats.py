
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields


class TestCase(UploadedTrackTestCase):

    def test_none_then_none_on_empty_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_empty_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_empty_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def none_then_none_on_filled_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def none_then_none_on_filled_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def none_then_none_on_filled_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC)
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_10_then_10_on_empty_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_empty_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100

    def test_10_then_10_on_empty_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100

    def test_10_then_10_on_filled_mp3(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_filled_wav(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100

    def test_10_then_10_on_filled_flac(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC, **{PostFields.RATING: 10})
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100
