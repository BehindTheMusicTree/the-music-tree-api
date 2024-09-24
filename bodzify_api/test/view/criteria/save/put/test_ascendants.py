#!/usr/bin/env python

import logging
from rest_framework import status
from bodzify_api.model.criteria.CriteriaAscendantRelation import AttributesLabel
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.put import Fields as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_from_being_root_to_first_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        ascendant_relations = updated_punk_genre.criteria_ascendant_relation_ascendants.all()  # type: ignore
        assert ascendant_relations[0].ascendant.uuid == rock_genre.uuid
        assert ascendant_relations[0].degree == 1

    def test_from_being_first_descendant_to_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)

        data = {PUT_FIELD.PARENT: ""}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        updated_punk_genre = Criteria.objects.get(uuid=punk_genre.uuid)
        updated_punk_genre.criteria_ascendant_relation_ascendants.count() == 0  # type: ignore

    def test_new_root_then_update_ascendants_of_descendants(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        updated_punkhardcore_genre = Criteria.objects.get(uuid=punkhardcore_genre.uuid)
        punkhardcore_ascendants_unordered = updated_punkhardcore_genre.criteria_ascendant_relation_ascendants.all()  # type: ignore
        punkhardcore_ascendants_ordered = punkhardcore_ascendants_unordered.order_by(AttributesLabel.DEGREE)
        assert len(punkhardcore_ascendants_ordered) == 2
        assert punkhardcore_ascendants_ordered[0].ascendant.uuid == punk_genre.uuid
        assert punkhardcore_ascendants_ordered[0].degree == 1
        assert punkhardcore_ascendants_ordered[1].ascendant.uuid == rock_genre.uuid
        assert punkhardcore_ascendants_ordered[1].degree == 2

    def test_new_ascendant_then_update_ascendants_of_last_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)
        frenchpunkhardcore_genre = self.model_fixture_factory.create_genre(name="French punk hardcore",
                                                                           parent=punkhardcore_genre)
        bretonpunkhardcore_genre = self.model_fixture_factory.create_genre(name="Breton punk hardcore",
                                                                           parent=frenchpunkhardcore_genre)

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        updated_bretonpunkhardcore_genre = Criteria.objects.get(uuid=bretonpunkhardcore_genre.uuid)
        bretonpunkhardcore_ascendants_unordered = \
            updated_bretonpunkhardcore_genre.criteria_ascendant_relation_ascendants.all()  # type: ignore
        bretonpunkhardcore_ascendants_ordered = \
            bretonpunkhardcore_ascendants_unordered.order_by(AttributesLabel.DEGREE)
        assert len(bretonpunkhardcore_ascendants_ordered) == 4
        assert bretonpunkhardcore_ascendants_ordered[0].ascendant.uuid == frenchpunkhardcore_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[0].degree == 1
        assert bretonpunkhardcore_ascendants_ordered[1].ascendant.uuid == punkhardcore_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[1].degree == 2
        assert bretonpunkhardcore_ascendants_ordered[2].ascendant.uuid == punk_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[2].degree == 3
        assert bretonpunkhardcore_ascendants_ordered[3].ascendant.uuid == rock_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[3].degree == 4

    def test_newly_root_then_update_ascendants_of_last_descendant(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=punk_genre)

        data = {PUT_FIELD.PARENT: ""}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        assert self.saved_genre.root == punk_genre
        updated_punkhardcore_genre = Criteria.objects.get(uuid=punkhardcore_genre.uuid)
        punkhardcore_ascendants_unordered = updated_punkhardcore_genre.criteria_ascendant_relation_ascendants.all()  # type: ignore
        punkhardcore_ascendants_ordered = punkhardcore_ascendants_unordered.order_by(AttributesLabel.DEGREE)
        assert len(punkhardcore_ascendants_ordered) == 1
        assert punkhardcore_ascendants_ordered[0].ascendant.uuid == punk_genre.uuid
        assert punkhardcore_ascendants_ordered[0].degree == 1
