#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.StringAttributeSaveTestCase import \
    StringAttributeSaveTestCase


class TestCase(StringAttributeSaveTestCase):

    def test_longest_then_ok(self):
        artist_name = "a" * settings.ARTIST_NAME_LENGTH_MAX
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist.name == artist_name

    def test_too_long_then_error(self):
        artist_name = "a" * (settings.ARTIST_NAME_LENGTH_MAX + 1)
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_then_none(self):
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: None
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist == None

    def test_existing(self):
        artist_name = "Kopoe"
        G(Artist, user=self.test_user, name=artist_name)
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist.name == artist_name

    def test_not_existing(self):
        artist_name = "hoho"
        data = {
            EXTRACT_FIELDS.ARTIST_NAME: artist_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist.name == artist_name
