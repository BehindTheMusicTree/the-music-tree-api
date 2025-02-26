from rest_framework import status

from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase


class TestCase(TagPlaylistTestCase):

    def test_combined_then_ok(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        tag_punk = self.model_fixture_factory.create_tag(name="Punk", parent=tag_fiesta)
        tag_punky = self.model_fixture_factory.create_tag(name="Punky", parent=tag_fiesta)

        response = self._get_tag_playlists(name='PU', parent=tag_fiesta.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_punk.name in result_names
        assert tag_punky.name in result_names
