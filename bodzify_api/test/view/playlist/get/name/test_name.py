#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import FOREIGN_MODEL_ATTRIBUTES_LABEL as \
    PLAYLIST_FOREIGN_MODEL_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_name_of_criteria(self):
        rock_criteria_name = "Rock"
        rock_genre = G(Criteria,
                      user=self.test_user,
                      name=rock_criteria_name,
                      type=CRITERIA_TYPES_ID.GENRE)
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        response = self.get_genre_playlist(playlist_uuid=rock_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[CRITERIA_ATTRIBUTES_LABEL.NAME] == rock_criteria_name
