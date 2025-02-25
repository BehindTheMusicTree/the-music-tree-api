from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import     TagPlaylistTestCase


class TestCase(TagPlaylistTestCase):

    def test_put_then_not_allowed(self):
        tag = self.model_fixture_factory.create_tag(name='fiesta')

        response = self._put_tag_playlist(tag.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
