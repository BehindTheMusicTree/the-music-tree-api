#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import FIELDS as POST_FIELDS


class TestCase(CriteriaTestCase):

    def test_parent_none_then_root_itself(self):
        data = {POST_FIELDS.NAME: "Rock"}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = self.model_fixture_factory.create_genre(name="Rock")
        data = {
            POST_FIELDS.NAME: "Punk",
            POST_FIELDS.PARENT: rock.uuid
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rockGenre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rockGenre)
        data = {
            POST_FIELDS.NAME: "Punk hardcore",
            POST_FIELDS.PARENT: punk_genre.uuid
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rockGenre
