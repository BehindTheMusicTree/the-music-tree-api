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

    def test_nullThenNone(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: None
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre == None

    def test_emptyThenNone(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: ""
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre == None

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.name == genreName
        
    def test_errorWhenTooLong(self):
        genreName = "a" * (settings.CRITERIA_NAME_MAX_CHAR + 1)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_existing(self):
        genreName = "Rock"
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: genreName})
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.uuid == self.saved_genre.uuid

    def test_newSoParentNone(self):
        genreName = "Rock"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.parent == None
