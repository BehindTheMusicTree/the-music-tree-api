from bodzify_api import settings
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.serializer.model.lib_track.input.Fields import Fields as Fields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = Fields.LANGUAGE
    lib_track_normalized_metadata_key = NormalizedMetadataKeys.LANGUAGE
    length_max = settings.LIB_TRACK_LANGUAGE_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
