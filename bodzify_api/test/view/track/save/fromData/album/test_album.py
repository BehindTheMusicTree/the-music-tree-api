#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_null_then_none(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "album_name" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album == None

    def test_empty_then_none(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "album_name" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album == None

    def test_longest(self):
        album_name = "a" * settings.ALBUM_NAME_LENGTH_MAX
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "album_name": album_name
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == album_name

    def test_existing(self):
        album_name = "Kopoe"
        G(Album, user=self.test_user, name=album_name)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "album_name": album_name,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == album_name

    def test_notExisting(self):
        album_name = "hoho"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "album_name": album_name,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.album.name == album_name
