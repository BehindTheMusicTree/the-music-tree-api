from bodzify_api import settings
from bodzify_api.serializer.model.uploaded_track.input.Fields import InputFields as InputFields
from bodzify_api.test.view.uploaded_track.input.update_file_metadata.LibTrackFileMetadataUpdateStrTestCase import (
    LibTrackFileMetadataUpdateStrTestCase
)
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(LibTrackFileMetadataUpdateStrTestCase):
    save_field = InputFields.TITLE
    uploaded_track_app_metadata_key = AppMetadataKey.TITLE
    length_max = settings.UPLOADED_TRACK_TITLE_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = '.mp3'


class FlacTestCase(TestCase):
    file_extension = '.flac'


class WavTestCase(TestCase):
    file_extension = '.wav'
