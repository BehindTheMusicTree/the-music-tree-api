#!/usr/bin/env python
from rest_framework import status
from bodzify_api import settings
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_longest(self):
        artistName = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ARTIST_NAME: artistName
        }
        response = self.postSampleTrack(sampleFilename="sample.wav", dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.savedTrackMetadata[key] == artistName

    def test_null(self):
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ARTIST_NAME: ""
        }
        response = self.postSampleTrack(sampleFilename="sample.wav", dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        key = AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME
        assert self.savedTrackMetadata[key] in ["", None]
