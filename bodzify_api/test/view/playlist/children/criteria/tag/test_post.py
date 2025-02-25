from rest_framework import status

from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import \
    TagPlaylistTestCase


class TestCase(TagPlaylistTestCase):

    def test_post_then_not_allowed(self):
        response = self._post_tag_playlist()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
