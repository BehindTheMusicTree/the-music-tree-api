
from bodzify_api import settings
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.serializer.schema.track.input.schema import Fields as SaveSchemaFields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = SaveSchemaFields.ALBUM_NAME
    lib_track_normalized_metadata_key = NormalizedMetadataKeys.ALBUM_NAME
    length_max = settings.ALBUM_NAME_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
