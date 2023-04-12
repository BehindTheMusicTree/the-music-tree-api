#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_TRACK_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_withCorrectSpacing(self):
        albumArtistsName = "Chuck Berry,  The Beatles,The Rolling Stones "
        data = {
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_NAME: "Chuck",
            SCHEMA_TRACK_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING: albumArtistsName
        }
        response = self.postSampleTrack(sampleFilename="sample.mp3", dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        albumArtistsKey = AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        assert self.savedTrackMetadata[albumArtistsKey] == "Chuck Berry,The Beatles,The Rolling Stones"
