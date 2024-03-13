#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria

logger = logging.getLogger('bodzify_api')


class TestCase(ApiViewTestCase):

    def test_from_being_root_to_first_descendant(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        assert updated_punk_genre.root == rock_genre

    def test_from_being_first_descendant_to_root(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE,
                       parent=rock_genre)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: ""
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        assert updated_punk_genre.root == punk_genre

    def test_new_root_then_update_root_of_descendants(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_hardcore_genre = G(Criteria,
                                name="Punk hardcore",
                                user=self.test_user,
                                type=CRITERIA_TYPES_ID.GENRE,
                                parent=punk_genre)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        assert updated_punk_genre.root == rock_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)
        assert updated_punk_hardcore_genre.root == rock_genre

    def test_new_ascendant_then_update_root_of_self_and_descendants(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_hardcore_genre = G(Criteria,
                                name="Punk hardcore",
                                user=self.test_user,
                                type=CRITERIA_TYPES_ID.GENRE,
                                parent=punk_genre)
        french_punk_hardcore_genre = G(Criteria,
                                       name="French punk hardcore",
                                       user=self.test_user,
                                       type=CRITERIA_TYPES_ID.GENRE,
                                       parent=punk_hardcore_genre)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        assert updated_punk_genre.root == rock_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)
        assert updated_punk_hardcore_genre.root == rock_genre
        updated_french_punk_hardcore_genre = Criteria.objects.get(uuid=french_punk_hardcore_genre.uuid)
        assert updated_french_punk_hardcore_genre.root == rock_genre

    def test_newly_root_then_update_root_of_descendants(self):
        rock_genre = G(Criteria,
                       name="Rock",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria,
                       name="Punk",
                       user=self.test_user,
                       type=CRITERIA_TYPES_ID.GENRE,
                       parent=rock_genre)
        punk_hardcore_genre = G(Criteria,
                                name="Punk hardcore",
                                user=self.test_user,
                                type=CRITERIA_TYPES_ID.GENRE,
                                parent=punk_genre)

        data = {
            CRITERIA_ATTRIBUTES_LABEL.PARENT: ""
        }
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.root == punk_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)
        assert updated_punk_hardcore_genre.root == punk_genre
