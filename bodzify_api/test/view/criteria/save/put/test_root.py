#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase

logger = logging.getLogger('bodzify_api')


class TestCase(CriteriaTestCase):

    def test_from_being_root_to_first_descendant(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)  # type: ignore
        assert updated_punk_genre.root == rock_genre

    def test_from_being_first_descendant_to_root(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)

        data = {PUT_FIELD.PARENT: ""}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)  # type: ignore
        assert updated_punk_genre.root == punk_genre

    def test_new_root_then_update_root_of_descendants(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_hardcore_genre = G(Criteria,
                                name="Punk hardcore",
                                user=self.test_user,
                                type=CRITERIA_TYPES_ID.GENRE,
                                parent=punk_genre)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)  # type: ignore
        assert updated_punk_genre.root == rock_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)  # type: ignore
        assert updated_punk_hardcore_genre.root == rock_genre

    def test_new_ascendant_then_update_root_of_self_and_descendants(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
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

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)  # type: ignore
        assert updated_punk_genre.root == rock_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)  # type: ignore
        assert updated_punk_hardcore_genre.root == rock_genre
        updated_french_punk_hardcore_genre = Criteria.objects.get(uuid=french_punk_hardcore_genre.uuid)  # type: ignore
        assert updated_french_punk_hardcore_genre.root == rock_genre

    def test_newly_root_then_update_root_of_descendants(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)
        punk_hardcore_genre = G(Criteria,
                                name="Punk hardcore",
                                user=self.test_user,
                                type=CRITERIA_TYPES_ID.GENRE,
                                parent=punk_genre)

        data = {PUT_FIELD.PARENT: ""}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_genre.root == punk_genre
        updated_punk_hardcore_genre = Criteria.objects.get(uuid=punk_hardcore_genre.uuid)  # type: ignore
        assert updated_punk_hardcore_genre.root == punk_genre
