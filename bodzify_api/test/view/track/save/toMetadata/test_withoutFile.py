#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


class WithoutFileTestCase(ApiViewTestCase):

    def test_okEvenWithoutAFile(self):
        track = G(LibraryTrack, 
                  user=self.testUser,
                  title="Foire",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            "title": "Jobo"
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
