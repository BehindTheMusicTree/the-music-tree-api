#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_ok(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        genre_new_name = "Punk"
        data = {PUT_FIELD.NAME: genre_new_name}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_200_OK # type: ignore
        saved_genre = Criteria.objects.get(uuid=rock_genre.uuid) # type: ignore
        assert saved_genre.name == genre_new_name

    def test_error_when_name_is_empty(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        data = {PUT_FIELD.NAME: ""}
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        saved_genre = Criteria.objects.get(uuid=rock_genre.uuid) # type: ignore
        assert saved_genre.name == "Rock"

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = G(Criteria, name=genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        response = self.put_genre(genre_uuid=genre.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK # type: ignore
        saved_genre = Criteria.objects.get(uuid=genre.uuid) # type: ignore
        assert saved_genre.name == genre_name
