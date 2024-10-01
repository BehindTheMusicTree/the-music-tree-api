#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.CriteriaAscendantRelation import AttributesLabel
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase
from bodzify_api.serializer.criteria.input.schema.endpoint.post import Fields as PostFields


class TestCase(CriteriaTestCase):

    def test_no_parent_provided_then_no_ascendants(self):
        data = {PostFields.NAME: "Rock"}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 0

    def test_root_parent_then_one_ascendant_with_degree_1(self):
        root = self.model_fixture_factory.create_genre(name="Rock")
        data = {PostFields.NAME: "Punk", PostFields.PARENT: root.uuid}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 1
        criteria_ascendant_relation = self.saved_genre.criteria_ascendant_relation_ascendants.all()[0]  # type: ignore
        assert criteria_ascendant_relation.ascendant.uuid == root.uuid
        assert criteria_ascendant_relation.degree == 1

    def test_child_of_child_of_root_then_three_ascendants(self):
        criteria1 = self.model_fixture_factory.create_genre(name="Rock")
        criteria2 = self.model_fixture_factory.create_genre(name="Soft rock", parent=criteria1)
        criteria3 = self.model_fixture_factory.create_genre(name="Pop rock", parent=criteria2)
        data = {PostFields.NAME: "Pop funk rock", PostFields.PARENT: criteria3.uuid}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 3
        criteria_ascendant_relations = self.saved_genre.criteria_ascendant_relation_ascendants.all()  # type: ignore
        criteria_ascendant_relations_ordered = criteria_ascendant_relations.order_by(AttributesLabel.DEGREE)
        assert criteria_ascendant_relations_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendant_relations_ordered[0].degree == 1
        assert criteria_ascendant_relations_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendant_relations_ordered[0].degree == 1
        assert criteria_ascendant_relations_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendant_relations_ordered[0].degree == 1
