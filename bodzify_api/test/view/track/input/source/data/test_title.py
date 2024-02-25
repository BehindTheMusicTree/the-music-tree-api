#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPutSerializer import \
    FIELDS as PUT_FIELDS
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_povided(self):
        title = "Mon Amour"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title=title,
                  duration=0)
        data = {}
        response = self.put_lib_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == title

    def test_nullThenNull(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Lolilom",
                  duration=0)
        data = {
            PUT_FIELDS.TITLE: None
        }
        response = self.put_lib_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == None

    def test_emptyThenNull(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Lolilom",
                  duration=0)
        data = {
            PUT_FIELDS.TITLE: ""
        }
        response = self.put_lib_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == None

    def test_longest(self):
        title = "a" * (settings.LIB_TRACK_LANGUAGE_LENGTH_MAX - len(".mp3"))
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Lolilom",
                  duration=0)
        data = {
            PUT_FIELDS.TITLE: title
        }
        response = self.put_lib_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == title
