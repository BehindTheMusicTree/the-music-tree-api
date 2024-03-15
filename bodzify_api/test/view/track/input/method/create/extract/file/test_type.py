#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.ApiTestCase import ApiViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS


class TestCase(ApiViewTestCase):

    def test_wav(self):
        response = self.extract_default_mine_track(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

    def test_mp3(self):
        response = self.extract_default_mine_track(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
