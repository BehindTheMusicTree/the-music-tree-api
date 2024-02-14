#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class ArtistTestCase(ApiViewTestCase):

    def test_deleteOldOneBecauseNothingLinkedToIt(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        data = {
            "artist_name": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(
            user=self.test_user, name=artist_name).count() == 0

    def test_notDeleteOldOneBecauseATrackLinkedToIt(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          artist=artist,
          duration=0)
        data = {
            "artist_name": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(
            user=self.test_user, name=artist_name).count() == 1

    def test_notDeleteOldOneBecauseAnAlbumLinkedToIt(self):
        artist_name = "a-ha"
        artist = G(Artist, user=self.test_user, name=artist_name)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  artist=artist,
                  duration=0)
        album = G(Album, user=self.test_user, name="Hunting High and Low", album_artists=[artist])
        G(LibraryTrack,
          user=self.test_user,
          title="Josie",
          album=album,
          duration=0)
        data = {
            "artist_name": "Paul",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(
            user=self.test_user, name=artist_name).count() == 1
