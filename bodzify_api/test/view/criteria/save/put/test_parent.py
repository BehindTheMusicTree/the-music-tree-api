#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.put import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_not_provided_then_unchanged(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.parent == rock_genre

    def test_error_when_parent_is_one_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punk_hardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        data = {PUT_FIELD.PARENT: punk_hardcore_genre.uuid}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_parent_is_itself(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
