from rest_framework import status

from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_with_parentA_and_children_then_set_children_parent_to_parentA(self):
        parent = self.model_fixture_factory.create_genre(name='parent')
        criteria = self.model_fixture_factory.create_genre(name='criteria', parent=parent)
        child_first = self.model_fixture_factory.create_genre(name='child first', parent=criteria)
        child_second = self.model_fixture_factory.create_genre(name='child second', parent=criteria)

        response = self._delete_genre(uuid=criteria.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        parent.refresh_from_db()
        assert parent.parent is None
        assert parent.children.count() == 2
        assert parent.children.filter(uuid=child_first.uuid).exists()
        assert parent.children.filter(uuid=child_second.uuid).exists()

        child_first.refresh_from_db()
        child_second.refresh_from_db()
        assert child_first.parent == parent
        assert child_second.parent == parent

    def test_delete_as_root_then_set_children_as_root(self):
        criteria = self.model_fixture_factory.create_genre(name='criteria')
        child_first = self.model_fixture_factory.create_genre(name='child first', parent=criteria)
        child_second = self.model_fixture_factory.create_genre(name='child second', parent=criteria)

        response = self._delete_genre(uuid=criteria.uuid)

        if response.status_code == 500:
            print("Response content:", response.content.decode())

        assert response.status_code == status.HTTP_204_NO_CONTENT

        child_first.refresh_from_db()
        assert child_first.parent is None
        assert child_first.is_root
        child_second.refresh_from_db()
        assert child_second.parent is None
        assert child_second.is_root

    def delete_then_update_ascendants_of_children(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='punk', parent=rock)
        hardcore = self.model_fixture_factory.create_genre(name='hardcore', parent=punk)

        assert punk.ascendants == [rock]
        assert hardcore.ascendants == [punk, rock]

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        punk.refresh_from_db()
        assert punk.ascendants == []
        hardcore.refresh_from_db()
        assert hardcore.ascendants == [punk]
