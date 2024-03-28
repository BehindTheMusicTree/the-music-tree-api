#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.CriteriaSaveSchemaSerializer import FIELDS as POST_FIELD
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_empty_then_none(self):
        data = {
            POST_FIELD.NAME: "Punk",
            POST_FIELD.PARENT: ""
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {
            POST_FIELD.NAME: "Punk",
            POST_FIELD.PARENT: rock_genre.uuid # type: ignore
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {
            POST_FIELD.NAME: "Punk",
            POST_FIELD.PARENT: "not existing"
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
