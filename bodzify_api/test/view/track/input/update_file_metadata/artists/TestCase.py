from bodzify_api import settings
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.serializer.schema.lib_track.input.Fields import Fields as Fields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase \
    import UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = Fields.ARTISTS_NAMES
    lib_track_normalized_metadata_key = NormalizedMetadataKeys.ARTISTS_NAMES
    length_max = settings.ARTIST_NAME_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
