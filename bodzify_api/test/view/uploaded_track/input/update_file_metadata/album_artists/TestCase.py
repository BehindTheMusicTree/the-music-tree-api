from bodzify_api import settings
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase
)
from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = PostFields.ALBUM_ARTISTS_NAMES_MULTIPART
    uploaded_track_app_metadata_key = AppMetadataKey.ALBUM_ARTISTS_NAMES
    length_max = settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX
    album_data = {PostFields.ALBUM_NAME: "The Great Twenty-Eight"}
    value_expected_in_metadata_is_list = True

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_data, file_has_metadata=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_data, file_has_metadata=True)

    def test_largest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data=self.album_data, file_has_metadata=False)


class Mp3TestCase(TestCase):
    file_extension = '.mp3'


class FlacTestCase(TestCase):
    file_extension = '.flac'


class WavTestCase(TestCase):
    file_extension = '.wav'
