from bodzify_api import settings
from bodzify_api.serializer.model.uploaded_track.input.Fields import Fields as Fields
from bodzify_api.test.view.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase
)
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = Fields.ALBUM_NAME
    uploaded_track_app_metadata_key = AppMetadataKey.ALBUM_NAME
    length_max = settings.ALBUM_NAME_LEN_MAX
    album_artists_data = {Fields.ALBUM_ARTISTS_NAMES_MULTIPART: ['Muse']}

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_artists_data, file_has_metadata=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_artists_data, file_has_metadata=True)

    def test_largest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data=self.album_artists_data, file_has_metadata=False)


class Mp3TestCase(TestCase):
    file_extension = '.mp3'


class FlacTestCase(TestCase):
    file_extension = '.flac'


class WavTestCase(TestCase):
    file_extension = '.wav'
