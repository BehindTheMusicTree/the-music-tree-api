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

    def test_notProvided(self):
        artist = G(Artist, user=self.testUser, name="Jojo")
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  artist=artist,
                  duration=0)
        response = self.put_sample_track(track.uuid, data={})
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.uuid == artist.uuid

    def test_nullThenNone(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: None
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist == None

    def test_empty(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: ""
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist == None

    def test_longest(self):
        artistName = "a" * settings.ARTIST_NAME_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artistName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.name == artistName

    def test_existing(self):
        artistName = "a-ha"
        G(Artist, user=self.testUser, name=artistName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artistName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.name == artistName

    def test_notExisting(self):
        artistName = "hoho"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME: artistName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.name == artistName
