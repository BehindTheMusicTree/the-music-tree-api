#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class GenreTestCase(ApiViewTestCase):

    def test_notProvided(self):
        self.postCriteria(dataJson={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.savedCriteria,
                  duration=0)
        data = {}
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.uuid == self.savedCriteria.uuid

    def test_noneThenShouldBeGenreless(self):
        url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL.URL: url,
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: None
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS

    def test_emptyThenShouldBeGenreless(self):
        url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL.URL: url,
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: ""
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS

    def test_longest(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL.URL: url,
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == genreName

    def test_existing(self):
        genreName = "Rock"
        rockGenre = self.postCriteria(
            dataJson={CRITERIA_ATTRIBUTES_LABEL.NAME: genreName})
        url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL.URL: url,
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.uuid == rockGenre.uuid

    def test_newSoParentAll(self):
        genreName = "Rock"
        url = "https://lasonotheque.org/UPLOAD/wav/0001.wav"
        data = {
            TRACK_EXTRACT_SCHEMA_ATTRIBUTES_LABEL.URL: url,
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.parent.name == CriteriaSpecialNames.GENRE_ALL
