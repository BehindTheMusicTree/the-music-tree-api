#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.criteria.input.schema.endpoint.post import Fields as PostFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_playlist_creation(self):
        genre_name = "Rock"
        data = {PostFields.NAME: genre_name}
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CriteriaPlaylist.objects.filter(user=self.test_user1, criteria__name=genre_name).exists()

    def test_playlist_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre_name = "Punk Hardcore"
        data = {PostFields.NAME: punkhardcore_genre_name, PostFields.PARENT: punk_genre.uuid}
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        punkhardcore_playlist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=punkhardcore_genre_name)
        assert punkhardcore_playlist.root == rock_genre.criteria_playlist
