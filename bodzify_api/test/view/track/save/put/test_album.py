#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


class AlbumTestCase(ApiViewTestCase):

    def test_deleteOldOneBecauseNothingLinkedToIt(self):
        albumName = "Le Noir"
        album = G(Album, user=self.testUser, name=albumName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Foire",
                  album=album,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            "albumName": "Paul",
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.testUser, name=albumName).count() == 0

    def test_notDeleteOldOneBecauseATrackLinkedToIt(self):
        albumName = "La Saucisse"
        album = G(Album, user=self.testUser, name=albumName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Foire",
                  album=album,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        G(LibraryTrack,
          user=self.testUser,
          title="Josie",
          album=album,
          genre=self.testUserGenrelessGenre,
          duration=0)
        data = {
            "albumName": "Paul",
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.testUser, name=albumName).count() == 1
