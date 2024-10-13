#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.criteria.Criteria import AttributesLabels
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_root(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        genre_json = self.results[0]
        assert genre_json[AttributesLabels.ROOT][AttributesLabels.UUID] == genre.uuid

    def test_root_of_first_descandant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        for json_element in self.results:
            if json_element[AttributesLabels.UUID] == punk_genre.uuid:
                assert json_element[AttributesLabels.ROOT][AttributesLabels.UUID] == rock_genre.uuid

    def test_root_of_second_descandant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk Hardcore", parent=punk_genre)
        response = self.get_genres()
        assert response.status_code == status.HTTP_200_OK
        for json_element in self.results:
            if json_element[AttributesLabels.UUID] == punkhardcore_genre.uuid:
                assert json_element[AttributesLabels.ROOT][AttributesLabels.UUID] == rock_genre.uuid
