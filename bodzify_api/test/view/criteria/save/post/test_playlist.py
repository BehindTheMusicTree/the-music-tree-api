#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):
        
    def test_playlist_creation(self):
        genre_name = "Rock"
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genre_name
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CriteriaPlaylist.objects.filter(
            user=self.test_user, 
            criteria__name=genre_name,
            type=CriteriaTypesId.GENRE).exists()
