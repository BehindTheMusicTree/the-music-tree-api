#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStringTestCase import \
    UpdateFileMetadataStringTestCase


class TestCase(UpdateFileMetadataStringTestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(save_field=SAVE_FIELDS.ARTIST_NAME,
                         metadata_dict_key=AudioMetadataManager.METADATA_DICT_KEYS.ARTIST_NAME,
                         file_extension='flac',
                         length_max=settings.ARTIST_NAME_LENGTH_MAX,
                         methodName=methodName)
