#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_null_then_none(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: None
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.genre == None

    def test_empty_then_none(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: ""
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.genre == None

    def test_longest(self):
        genre_name = "a" * settings.CRITERIA_NAME_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.genre.name == genre_name
        
    def test_error_when_too_long(self):
        genre_name = "a" * (settings.CRITERIA_NAME_MAX_CHAR + 1)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_existing(self):
        genre_name = "Rock"
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: genre_name})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.genre.uuid == self.saved_genre.uuid

    def test_new_so_parent_none(self):
        genre_name = "Rock"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.genre.parent == None
