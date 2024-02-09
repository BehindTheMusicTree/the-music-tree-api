#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_parentNoneWhenNoParentProvided(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent.name == None
        
    def test_playlistCreation(self):
        genreName = "Rock"
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genreName
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert GenrePlaylist.objects.filter(
            user=self.test_user, criteria__name=genreName).exists()
