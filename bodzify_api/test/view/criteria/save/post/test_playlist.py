#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.criteria.input.schema.endpoint.post import Fields as POST_FIELDS
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_playlist_creation(self):
        genre_name = "Rock"
        data = {POST_FIELDS.NAME: genre_name}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CriteriaPlaylist.objects.filter(criteria__name=genre_name).exists()

    def test_playlist_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre_name = "Punk Hardcore"
        data = {POST_FIELDS.NAME: punkhardcore_genre_name, POST_FIELDS.PARENT: punk_genre.uuid}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        punkhardcore_playlist = CriteriaPlaylist.objects.get(criteria__name=punkhardcore_genre_name)
        assert punkhardcore_playlist.root == rock_genre.criteria_playlist  # type: ignore
