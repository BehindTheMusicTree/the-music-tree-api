#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria


class TestCase(ApiViewTestCase):

    def test_parent_none_then_root_itself(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == self.saved_genre

    def test_one_acendant_then_root_is_parent(self):
        rock = G(Criteria,
                 name="Rock",
                 user=self.test_user,
                 type=CRITERIA_TYPES_ID.GENRE)
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock.uuid
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rock

    def test_two_acendant_then_root_is_parent_of_parent(self):
        rockGenre = G(Criteria,
                      name="Rock",
                      user=self.test_user,
                      type=CRITERIA_TYPES_ID.GENRE)
        punkGenre = G(Criteria,
                      name="Punk",
                      user=self.test_user,
                      type=CRITERIA_TYPES_ID.GENRE,
                      parent=rockGenre)
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk hardcore",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: punkGenre.uuid
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == rockGenre
