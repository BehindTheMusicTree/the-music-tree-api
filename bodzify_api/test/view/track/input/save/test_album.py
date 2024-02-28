#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.StringAttributeSaveTestCase import \
    StringAttributeSaveTestCase


class TestCase(StringAttributeSaveTestCase):

    def test_longest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LENGTH_MAX
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: album_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album.name == album_name

    def test_too_long_then_error(self):
        album_name = "a" * (settings.ALBUM_NAME_LENGTH_MAX + 1)
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: album_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_then_none(self):
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: None
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album == None

    def test_existing(self):
        album_name = "Kopoe"
        G(Album, user=self.test_user, name=album_name)
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: album_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album.name == album_name

    def test_not_existing(self):
        album_name = "hoho"
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: album_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album.name == album_name
