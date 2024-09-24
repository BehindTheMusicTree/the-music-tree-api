#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.put import Fields as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_ok(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"
        data = {PUT_FIELD.NAME: genre_new_name}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        saved_genre = Criteria.objects.get(uuid=rock_genre.uuid)
        assert saved_genre.name == genre_new_name

    def test_error_when_name_is_empty(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        data = {PUT_FIELD.NAME: ""}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        saved_genre = Criteria.objects.get(uuid=rock_genre.uuid)
        assert saved_genre.name == "Rock"

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        response = self.put_genre(genre_uuid=genre.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        saved_genre = Criteria.objects.get(uuid=genre.uuid)
        assert saved_genre.name == genre_name
