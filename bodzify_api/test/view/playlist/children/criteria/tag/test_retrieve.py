from rest_framework import status

from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import \
    Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import \
    TagPlaylistTestCase


class TestCase(TagPlaylistTestCase):

    def test_retrieve_then_ok(self):
        tag_fiesta_name = "Fiesta"
        tag_fiesta = self.model_fixture_factory.create_tag(name=tag_fiesta_name)

        response = self._retrieve_tag_playlist(uuid=tag_fiesta.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RietrieveFields.NAME] == tag_fiesta_name
