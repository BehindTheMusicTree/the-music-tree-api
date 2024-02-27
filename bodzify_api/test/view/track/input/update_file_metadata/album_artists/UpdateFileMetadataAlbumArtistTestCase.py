#!/usr/bin/env python

from rest_framework import status

import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataStrTestCase import \
    UpdateFileMetadataStrTestCase


class UpdateFileMetadataAlbumArtistTestCase(UpdateFileMetadataStrTestCase):

    def __init__(self, file_extension: str, methodName: str = "runTest") -> None:
        super().__init__(save_field=SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                         metadata_dict_key=AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES,
                         file_extension=file_extension,
                         length_max=settings.ALBUM_ARTISTS_FIELD_LENGTH_MAX,
                         methodName=methodName)

    def test_on_missing_tag_then_ok(self, additional_data_json=None):
        additional_data_json = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck"
        }
        return super().test_on_missing_tag_then_ok(additional_data_json)

    def test_on_present_tag_then_ok(self, additional_data_json=None):
        additional_data_json = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck"
        }
        return super().test_on_present_tag_then_ok(additional_data_json)

    def test_longest_then_ok(self, additional_data_json=None):
        additional_data_json = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck"
        }
        return super().test_longest_then_ok(additional_data_json)

    def test_none_then_none(self, additional_data_json=None):
        additional_data_json = {
            SAVE_FIELDS.ALBUM_NAME: "Chuck"
        }
        return super().test_none_then_none(additional_data_json)
