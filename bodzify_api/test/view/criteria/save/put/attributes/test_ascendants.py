from django.db.models import QuerySet
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import \
    CriteriaLineageRel
from bodzify_api.model.criteria.lineage_rel.Fields import Fields
from bodzify_api.serializer.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_from_being_root_to_first_descendant(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK
        updated_genre_punk: Criteria = Criteria.objects.get(user=self.test_user1, uuid=genre_punk.uuid)
        ascendant_relations: QuerySet[CriteriaLineageRel] = \
            updated_genre_punk.ascendants_rels.all()
        assert ascendant_relations[0].ascendant.uuid == genre_rock.uuid
        assert ascendant_relations[0].degree == 1

    def test_from_being_first_descendant_to_root(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ""})
        assert response.status_code == status.HTTP_200_OK
        updated_genre_punk: Criteria = Criteria.objects.get(user=self.test_user1, uuid=genre_punk.uuid)
        assert updated_genre_punk.ascendants_rels.count() == 0

    def test_new_root_then_update_ascendants_of_descendants(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK

        updated_punkhardcore_genre: Criteria = Criteria.objects.get(uuid=punkhardcore_genre.uuid)
        punkhardcore_ascendants_unordered: QuerySet[CriteriaLineageRel] = \
            updated_punkhardcore_genre.ascendants_rels.all()
        punkhardcore_ascendants_ordered = punkhardcore_ascendants_unordered.order_by(Fields.DEGREE)
        assert len(punkhardcore_ascendants_ordered) == 2
        assert punkhardcore_ascendants_ordered[0].ascendant.uuid == genre_punk.uuid
        assert punkhardcore_ascendants_ordered[0].degree == 1
        assert punkhardcore_ascendants_ordered[1].ascendant.uuid == genre_rock.uuid
        assert punkhardcore_ascendants_ordered[1].degree == 2

    def test_new_ascendant_then_update_ascendants_of_last_descendant(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)
        frenchpunkhardcore_genre = self.model_fixture_factory.create_genre(name="French punk hardcore",
                                                                           parent=punkhardcore_genre)
        bretonpunkhardcore_genre = self.model_fixture_factory.create_genre(name="Breton punk hardcore",
                                                                           parent=frenchpunkhardcore_genre)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK

        updated_bretonpunkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1,
                                                                          uuid=bretonpunkhardcore_genre.uuid)
        bretonpunkhardcore_ascendants_unordered: QuerySet[CriteriaLineageRel] = \
            updated_bretonpunkhardcore_genre.ascendants_rels.all()
        bretonpunkhardcore_ascendants_ordered = \
            bretonpunkhardcore_ascendants_unordered.order_by(Fields.DEGREE)
        assert len(bretonpunkhardcore_ascendants_ordered) == 4
        assert bretonpunkhardcore_ascendants_ordered[0].ascendant.uuid == frenchpunkhardcore_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[0].degree == 1
        assert bretonpunkhardcore_ascendants_ordered[1].ascendant.uuid == punkhardcore_genre.uuid
        assert bretonpunkhardcore_ascendants_ordered[1].degree == 2
        assert bretonpunkhardcore_ascendants_ordered[2].ascendant.uuid == genre_punk.uuid
        assert bretonpunkhardcore_ascendants_ordered[2].degree == 3
        assert bretonpunkhardcore_ascendants_ordered[3].ascendant.uuid == genre_rock.uuid
        assert bretonpunkhardcore_ascendants_ordered[3].degree == 4

    def test_newly_root_then_update_ascendants_of_last_descendant(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punkhardcore_genre = self.model_fixture_factory.create_genre(name="Punk hardcore", parent=genre_punk)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ""})
        assert response.status_code == status.HTTP_200_OK

        assert self.saved_object.root == genre_punk
        updated_punkhardcore_genre: Criteria = Criteria.objects.get(user=self.test_user1, uuid=punkhardcore_genre.uuid)
        punkhardcore_ascendants_ordered = updated_punkhardcore_genre.ascendants_rels.all().order_by(Fields.DEGREE)
        assert len(punkhardcore_ascendants_ordered) == 1
        assert punkhardcore_ascendants_ordered[0].ascendant.uuid == genre_punk.uuid
        assert punkhardcore_ascendants_ordered[0].degree == 1
