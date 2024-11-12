from rest_framework import status
from django.db.models import QuerySet

from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from bodzify_api.model.criteria.lineage_rel.Fields import Fields
from bodzify_api.serializer.schema.criteria.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_no_parent_provided_then_no_ascendants(self):
        data = {PostFields.NAME: "Rock"}
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 0

    def test_root_parent_then_one_ascendant_with_degree_1(self):
        root = self.model_fixture_factory.create_genre(name="Rock")
        data = {PostFields.NAME: "Punk", PostFields.PARENT: root.uuid}
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 1
        criteria_lineage_rel: CriteriaLineageRel = self.saved_genre.ascendants_rels.all()[0]
        assert criteria_lineage_rel.ascendant.uuid == root.uuid
        assert criteria_lineage_rel.degree == 1

    def test_child_of_child_of_root_then_three_ascendants(self):
        criteria1 = self.model_fixture_factory.create_genre(name="Rock")
        criteria2 = self.model_fixture_factory.create_genre(name="Soft rock", parent=criteria1)
        criteria3 = self.model_fixture_factory.create_genre(name="Pop rock", parent=criteria2)
        data = {PostFields.NAME: "Pop funk rock", PostFields.PARENT: criteria3.uuid}
        response = self._post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.ascendants.count() == 3
        criteria_ascendants_rels: QuerySet[CriteriaLineageRel] = \
            self.saved_genre.ascendants_rels.all()
        criteria_ascendants_rels_ordered = criteria_ascendants_rels.order_by(Fields.DEGREE)
        assert criteria_ascendants_rels_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendants_rels_ordered[0].degree == 1
        assert criteria_ascendants_rels_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendants_rels_ordered[0].degree == 1
        assert criteria_ascendants_rels_ordered[0].ascendant.uuid == criteria3.uuid
        assert criteria_ascendants_rels_ordered[0].degree == 1
