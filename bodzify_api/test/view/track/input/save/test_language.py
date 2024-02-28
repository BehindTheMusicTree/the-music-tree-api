#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.StringAttributeSaveTestCase import \
    StringAttributeSaveTestCase


class TestCase(StringAttributeSaveTestCase):

    def test_longest_then_ok(self):
        language = "a" * settings.LIB_TRACK_LANGUAGE_LENGTH_MAX
        data = {
            PUT_FIELDS.LANGUAGE: language
        }
        response = self.extract_default_mine_track(data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == language

    def test_too_long_then_error(self):
        language = "a" * (settings.LIB_TRACK_LANGUAGE_LENGTH_MAX + 1)
        data = {
            PUT_FIELDS.LANGUAGE: language
        }
        response = self.extract_default_mine_track(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_then_none(self):
        data = {
            PUT_FIELDS.LANGUAGE: None
        }
        response = self.extract_default_mine_track(data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.language == None
