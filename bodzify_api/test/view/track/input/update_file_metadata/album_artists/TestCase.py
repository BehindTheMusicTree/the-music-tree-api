from bodzify_api import settings
from bodzify_api.utils.audio_metadata.AppMetadataKey import AppMetadataKey
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase \
    import UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = PostFields.ALBUM_ARTISTS_NAMES_ARRAY
    lib_track_app_metadata_key = AppMetadataKey.ALBUM_ARTISTS_NAMES_STR
    length_max = settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX
    album_data_dict = {PostFields.ALBUM_NAME: "The Great Twenty-Eight"}

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data_dict=self.album_data_dict, file_has_tags=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data_dict=self.album_data_dict, file_has_tags=True)

    def test_longest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data_dict=self.album_data_dict, file_has_tags=False)


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
