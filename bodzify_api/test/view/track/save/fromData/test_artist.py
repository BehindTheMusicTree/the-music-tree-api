#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        artist = G(Artist, user=self.test_user, name="Jojo")
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  artist=artist,
                  duration=0)
        response = self.put_sample_track(track.uuid, data_json={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist.uuid == artist.uuid

    def test_null_then_none(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: None
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist == None

    def test_empty_then_none(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: ""
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist == None

    def test_longest(self):
        artist_name = "a" * settings.ARTIST_NAME_LENGTH_MAX
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist.name == artist_name

    def test_existing(self):
        artist_name = "a-ha"
        G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist.name == artist_name

    def test_not_existing(self):
        artist_name = "hoho"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artist_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.artist.name == artist_name
