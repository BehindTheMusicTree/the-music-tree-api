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

    def test_nullThenNone(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName" : None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album == None

    def test_emptyThenNone(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album == None

    def test_longest(self):
        albumName = "a" * settings.ALBUM_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == albumName

    def test_existing(self):
        albumName = "Kopoe"
        G(Album, user=self.test_user, name=albumName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == albumName

    def test_notExisting(self):
        albumName = "hoho"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "albumName": albumName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == albumName
