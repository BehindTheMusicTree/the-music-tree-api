#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenUnchanged(self):
        album = G(Album, user=self.test_user, name="Jojo")
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  album=album,
                  duration=0)
        data = {}
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.uuid == album.uuid

    def test_deleteOldOneBecauseNothingLinkedToIt(self):
        albumName = "Le Noir"
        album = G(Album, user=self.test_user, name=albumName)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  album=album,
                  duration=0)
        data = {
            "albumName": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.test_user, name=albumName).count() == 0

    def test_notDeleteOldOneBecauseATrackLinkedToIt(self):
        albumName = "La Saucisse"
        album = G(Album, user=self.test_user, name=albumName)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  album=album,
                  duration=0)
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          album=album,
          duration=0)
        data = {
            "albumName": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.test_user, name=albumName).count() == 1
