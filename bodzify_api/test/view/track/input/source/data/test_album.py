#!/usr/bin/env python

from rest_framework import status
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.track.input.source.data.LibTrackAttributeFromDataTestCase import \
    LibTrackAttributeFromDataTestCase


class TestCase(LibTrackAttributeFromDataTestCase):

    def test_not_empty_then_ok(self):
        album_name = 'a'
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: album_name
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_ok(self):
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: ''
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_null_then_ok(self):
        data = {
            EXTRACT_FIELDS.ALBUM_NAME: None
        }
        response = self.extract_default_mine_track(json_data=data)
        assert response.status_code == status.HTTP_201_CREATED
