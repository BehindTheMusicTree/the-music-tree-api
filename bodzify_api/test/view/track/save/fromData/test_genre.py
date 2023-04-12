#!/usr/bin/env python
import pprint
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_nullThenNone(self):
        self.postGenre(dataJson={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.savedGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: None
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre == None

    def test_emptyThenNone(self):
        self.postGenre(dataJson={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.savedGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: ""
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre == None

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.name == genreName

    def test_existing(self):
        genreName = "Rock"
        self.postGenre(dataJson={CRITERIA_ATTRIBUTES_LABEL.NAME: genreName})
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.savedGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.uuid == self.savedGenre.uuid

    def test_newSoParentAll(self):
        genreName = "Rock"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.parent.name == CriteriaSpecialNames.GENRE_ALL
