#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenGenreless(self):
        response = self.postSampleTrack(sampleFilename="notProvided.mp3", dataJson={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
