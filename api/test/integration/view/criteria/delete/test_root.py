from rest_framework import status

from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_as_root_then_update_descendants_root(self):
        rock = self.model_fixture_factory.create_genre(name='rock')

        # Save genres and their UUIDs before deletion for later retrieval
        punk = self.model_fixture_factory.create_genre(name='punk', parent=rock)
        punk_uuid = punk.uuid

        hardcore_punk = self.model_fixture_factory.create_genre(name='hardcore punk', parent=punk)
        hardcore_punk_uuid = hardcore_punk.uuid

        indie = self.model_fixture_factory.create_genre(name='indie', parent=rock)
        indie_uuid = indie.uuid

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # The rock genre no longer exists, don't try to refresh it
        # Instead, re-fetch the children by UUID to check their new state
        punk = self.model_class.objects.get(user=self.test_user1, uuid=punk_uuid)
        hardcore_punk = self.model_class.objects.get(user=self.test_user1, uuid=hardcore_punk_uuid)
        indie = self.model_class.objects.get(user=self.test_user1, uuid=indie_uuid)

        # After parent deletion, these should be root genres with self as root
        assert punk.parent is None
        assert indie.parent is None

        # Verify root relationships
        assert punk.root == punk
        assert hardcore_punk.root == punk
        assert indie.root == indie
