from bodzify_api import settings
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.serializer.schema.model.lib_track.input.Fields import Fields as InputFields
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase \
    import UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):
    save_field = InputFields.GENRE_NAME
    lib_track_normalized_metadata_key = NormalizedMetadataKeys.GENRE_NAME
    length_max = settings.CRITERIA_NAME_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = 'mp3'


class FlacTestCase(TestCase):
    file_extension = 'flac'


class WavTestCase(TestCase):
    file_extension = 'wav'
