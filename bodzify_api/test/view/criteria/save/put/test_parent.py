#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_not_provided_then_unchanged(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)
        data = {}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_200_OK # type: ignore
        assert self.saved_genre.parent == rock_genre

    def test_error_when_parent_is_one_of_descendants(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)
        punkHardcoreGenre = G(Criteria,
                              name="Punk hardcore",
                              user=self.test_user,
                              type=CRITERIA_TYPES_ID.GENRE,
                              parent=punk_genre)

        data = {PUT_FIELD.PARENT: punkHardcoreGenre.uuid} # type: ignore
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore

    def test_error_when_parent_is_itself(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {PUT_FIELD.PARENT: rock_genre.uuid} # type: ignore
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
