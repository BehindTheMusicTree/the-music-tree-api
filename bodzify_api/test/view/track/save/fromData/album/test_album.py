#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class ArtistTestCase(ApiViewTestCase):

    def test_notProvided(self):
        album = G(Artist, user=self.testUser, name="Jojo")
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  album=album,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.album.uuid == album.uuid

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName" : None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album == None

    def test_empty(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album == None

    def test_longest(self):
        albumName = "a" * settings.ALBUM_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.name == albumName

    def test_existing(self):
        albumName = "Kopoe"
        G(Album, user=self.testUser, name=albumName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.name == albumName

    def test_notExisting(self):
        albumName = "hoho"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.album.name == albumName
