#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.test.ApiTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_playlist_creation(self):
        genre_name = "Rock"
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genre_name
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CriteriaPlaylist.objects.filter(criteria__name=genre_name).exists()
