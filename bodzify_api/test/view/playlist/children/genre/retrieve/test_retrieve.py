#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithTracksSerializer \
    import FIELDS as GET_RESULT_FIELDS
from bodzify_api.test.view.playlist.children.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):

    def test_ok(self):
        rock_criteria_name = "Rock"
        rock_genre = self.model_fixture_factory.create_genre(name=rock_criteria_name)
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).base_playlist
        response = self.retrieve_genre_playlist(playlist_uuid=rock_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[GET_RESULT_FIELDS.NAME] == rock_criteria_name  # type: ignore
