
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields


class TestCase(LibTrackTestCase):

    def test_0_then_0_on_mp3(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 0})
        assert response.status_code == 201
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 0

    def test_0_then_0_on_wav(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_WAV, **{PostFields.RATING: 0})
        assert response.status_code == 201
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 0

    def test_0_then_0_on_flac(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 0})
        assert response.status_code == 201
        assert self.saved_object.track_file
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 0

    def test_5_then_5_on_mp3(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PostFields.RATING: 5})
        assert response.status_code == 201
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 5

    def test_5_then_5_on_wav(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_WAV, **{PostFields.RATING: 5})
        assert response.status_code == 201
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 5

    def test_5_then_5_on_flac(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_FLAC, **{PostFields.RATING: 5})
        assert response.status_code == 201
        assert self.saved_lib_track_metadata[AppMetadataKey.RATING] == 5
