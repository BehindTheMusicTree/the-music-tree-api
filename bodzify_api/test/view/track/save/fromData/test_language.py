#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class LanguageTestCase(ApiViewTestCase):

    def test_notProvided(self):
        language = "French"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  language=language,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.language == language

    def test_null(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "language" : None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.language == ""

    def test_empty(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "language" : ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.language == ""

    def test_longest(self):
        language = "a" * settings.TRACK_LANGUAGE_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "language": language
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.language == language
