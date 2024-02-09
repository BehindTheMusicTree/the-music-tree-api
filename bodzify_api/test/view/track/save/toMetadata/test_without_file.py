#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TestCase(ApiViewTestCase):

    def test_ok_even_without_a_file(self):
        track = G(LibraryTrack, 
                  user=self.test_user,
                  title="Foire",
                  duration=0)
        data = {
            "title": "Jobo"
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
