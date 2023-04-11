#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
    ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvided(self):
        title = "Mon Amour"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title=title,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == title

    def test_nullThenNull(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Lolilom",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.TITLE: None
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == None

    def test_emptyThenNull(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Lolilom",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.TITLE: ""
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == None

    def test_longest(self):
        title = "a" * (settings.TRACK_LANGUAGE_MAX_CHAR - len(".mp3"))
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Lolilom",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.TITLE: title
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == title
