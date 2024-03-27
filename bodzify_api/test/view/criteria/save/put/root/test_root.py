#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_parent_none_then_root_itself(self):
        data = {PUT_FIELD.NAME: "Rock"}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = G(Criteria,
                 name="Rock",
                 user=self.test_user,
                 type=CRITERIA_TYPES_ID.GENRE)
        data = {
            PUT_FIELD.NAME: "Punk",
            PUT_FIELD.PARENT: rock.uuid # type: ignore
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rockGenre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punkGenre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rockGenre)
        data = {
            PUT_FIELD.NAME: "Punk hardcore",
            PUT_FIELD.PARENT: punkGenre.uuid # type: ignore
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_genre.root == rockGenre
