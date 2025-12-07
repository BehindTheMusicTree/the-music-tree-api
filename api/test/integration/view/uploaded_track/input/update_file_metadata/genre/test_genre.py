from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackTestCase):

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

    def test_wav_then_ok(self):
        genre_name = 'Pop'
        data = {PostFields.GENRE: genre_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == genre_name
