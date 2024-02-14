#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_povidedThenUnchanged(self):
        album = G(Album, user=self.test_user, name="Jojo")
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  album=album,
                  duration=0)
        data = {}
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track.album.uuid == album.uuid

    def test_deleteOldOneBecauseNothingLinkedToIt(self):
        album_name = "Le Noir"
        album = G(Album, user=self.test_user, name=album_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  album=album,
                  duration=0)
        data = {
            "album_name": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.test_user, name=album_name).count() == 0

    def test_notDeleteOldOneBecauseATrackLinkedToIt(self):
        album_name = "La Saucisse"
        album = G(Album, user=self.test_user, name=album_name)
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
            "album_name": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(
            user=self.test_user, name=album_name).count() == 1
