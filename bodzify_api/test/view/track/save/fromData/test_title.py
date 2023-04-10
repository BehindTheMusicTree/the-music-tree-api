#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TitleTestCase(ApiViewTestCase):

    def test_notProvided(self):
        title = "Mon Amour"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title=title,
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == title

    def test_errorWhenNull(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "title" : None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == ""

    def test_empty(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "title" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == ""

    def test_longest(self):
        title = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "title": title
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == title
