
from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase


class TestCase(TagPlaylistTestCase):

    def test_post_then_not_allowed(self):
        tag = self.model_fixture_factory.create_tag(name='fiesta')

        response = self._delete_tag_playlist(uuid=tag.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
