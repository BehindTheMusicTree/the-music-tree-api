#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


class GenreTestCase(ApiViewTestCase):

    def test_notProvided(self):
        genre = G(Criteria, user=self.testUser,
                  type=CriteriaTypesId.GENRE, name="Rock")
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=genre,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.uuid == genre.uuid

    def test_noneThenShouldBeGenreless(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS

    def test_emptyThenShouldBeGenreless(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == genreName

    def test_existing(self):
        genreName = "Rock"
        genre = G(Criteria, user=self.testUser, type=CriteriaTypesId.GENRE, name=genreName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.uuid == genre.uuid

    def test_newSoParentAll(self):
        genreName = "Rock"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.parent.name == CriteriaSpecialNames.GENRE_ALL
