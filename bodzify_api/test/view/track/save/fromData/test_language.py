#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
    ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvided(self):
        language = "French"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  language=language,
                  duration=0)
        data = {}
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == language

    def test_nullThenNone(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.LANGUAGE: None
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == None

    def test_emptyThenNone(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.LANGUAGE: ""
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == None

    def test_longest(self):
        language = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_ATTRIBUTES_LABEL.LANGUAGE: language
        }
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == language
