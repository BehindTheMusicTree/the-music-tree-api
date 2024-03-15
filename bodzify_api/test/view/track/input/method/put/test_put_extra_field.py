#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase


class TestCase(ApiTestCase):

    def test_error(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  duration=0)
        data = {
            "nonExistingField": "oifjqoif",
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
