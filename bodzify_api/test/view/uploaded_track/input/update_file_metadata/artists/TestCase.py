from bodzify_api import settings
from bodzify_api.serializer.model.uploaded_track.input.Fields import Fields as Fields
from bodzify_api.test.view.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase
)
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = Fields.ARTISTS_NAMES_MULTIPART
    uploaded_track_app_metadata_key = AppMetadataKey.ARTISTS_NAMES
    length_max = settings.ARTIST_NAME_LEN_MAX
    value_expected_in_metadata_is_list = True


class Mp3TestCase(TestCase):
    file_extension = '.mp3'


class FlacTestCase(TestCase):
    file_extension = '.flac'


class WavTestCase(TestCase):
    file_extension = '.wav'
