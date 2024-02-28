#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL, LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        title = "Mon Amour"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title=title,
                  duration=0)
        data = {}
        response = self.put_lib_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == title

    def test_ok(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      duration=0)
        lib_track_title_new = "hey ya"
        data = {
            ATTRIBUTES_LABEL.TITLE: lib_track_title_new
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == lib_track_title_new

    def test_empty_then_none(self):
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      duration=0)
        lib_track_title_new = "hey ya"
        data = {
            ATTRIBUTES_LABEL.TITLE: ''
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == None
