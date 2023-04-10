#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


class ArtistTestCase(ApiViewTestCase):

    def test_notProvided(self):
        artist = G(Artist, user=self.testUser, name="Jojo")
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  artist=artist,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.artist.uuid == artist.uuid

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "artistName" : None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist == None

    def test_empty(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "artistName" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist == None

    def test_longest(self):
        artistName = "a" * settings.ARTIST_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "artistName": artistName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == artistName

    def test_existing(self):
        artistName = "a-ha"
        G(Artist, user=self.testUser, name=artistName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "artistName": artistName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == artistName

    def test_notExisting(self):
        artistName = "hoho"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "artistName": artistName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.artist.name == artistName
