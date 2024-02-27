#!/usr/bin/env python

from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class TestCase(UpdateFileMetadataStrTestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(save_field=SAVE_FIELDS.ALBUM_NAME,
                         metadata_dict_key=AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_NAME,
                         file_extension='mp3',
                         length_max=settings.ALBUM_NAME_LENGTH_MAX,
                         methodName=methodName)
