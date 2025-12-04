from bodzify_api import settings
from bodzify_api.serializer.model.uploaded_track.input.Fields import Fields as Fields
from bodzify_api.test.view.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase
)
from bodzify_api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = Fields.TITLE
    uploaded_track_app_metadata_key = AppMetadataKey.TITLE
    length_max = settings.UPLOADED_TRACK_TITLE_LEN_MAX


class Mp3TestCase(TestCase):
    file_extension = '.mp3'


class FlacTestCase(TestCase):
    file_extension = '.flac'


class WavTestCase(TestCase):
    file_extension = '.wav'
