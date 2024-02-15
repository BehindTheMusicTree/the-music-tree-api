#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria


class TestCase(ApiViewTestCase):

    def test_not_provided_then_unchanged(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        punk_genre = G(Criteria, 
            name="Punk", 
            user=self.test_user, 
            type=CriteriaTypesId.GENRE, 
            parent=rock_genre)
        data = {}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.parent == rock_genre

    def test_error_when_parent_is_one_of_descendants(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        punk_genre = G(Criteria,
            name="Punk",
            user=self.test_user,
            type=CriteriaTypesId.GENRE,
            parent=rock_genre)
        punkHardcoreGenre = G(Criteria,
            name="Punk hardcore",
            user=self.test_user,
            type=CriteriaTypesId.GENRE,
            parent=punk_genre)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: punkHardcoreGenre.uuid
        }
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_error_when_parent_is_itself(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=rock_genre.uuid, data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
