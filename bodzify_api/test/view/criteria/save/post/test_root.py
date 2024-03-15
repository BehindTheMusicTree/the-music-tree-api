#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria


class TestCase(ApiTestCase):

    def test_parent_none_then_root_itself(self):
        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        response = self.post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = G(Criteria,
                 name="Rock",
                 user=self.test_user,
                 type=CRITERIA_TYPES_ID.GENRE)
        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock.uuid  # type: ignore
        }
        response = self.post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE,
                       parent=rock_genre)
        data_dict = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk hardcore",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: punk_genre.uuid  # type: ignore
        }
        response = self.post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.root == rock_genre
