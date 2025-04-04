from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(LibTrackTestCase):

    def test_mp3_then_ok(self):
        genre_name = 'metal'
        data = {PostFields.GENRE: genre_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == genre_name

    def test_flac_then_ok(self):
        genre_name = 'metal'
        data = {PostFields.GENRE: genre_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == genre_name

    def test_wav_with_handled_genre_code_then_ok(self):
        genre_name = 'Pop'
        data = {PostFields.GENRE: genre_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == genre_name

    def test_wav_with_handled_genre_code_but_with_different_case_then_ok(self):
        data = {PostFields.GENRE: 'pop'}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == 'Pop'

    def test_wav_with_not_handled_genre_code_then_other(self):
        data = {PostFields.GENRE: 'Liquid Techno'}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == 'Other'
