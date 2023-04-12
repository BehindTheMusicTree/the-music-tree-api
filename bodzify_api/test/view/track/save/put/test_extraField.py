#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class ExtraFieldTestCase(ApiViewTestCase):

    def test_error(self):
        track = G(LibraryTrack, 
                  user=self.testUser,
                  title="Foire",
                  duration=0)
        data = {
            "nonExistingField": "oifjqoif",
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
