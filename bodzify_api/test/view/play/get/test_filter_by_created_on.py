from rest_framework import status

from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.filter.set.private_unique_resource.Fields import Fields


class TestCase(PlayTestCase):

    def test_filter_then_ok(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        self.model_fixture_factory.create_play(content_object=track)
        self.model_fixture_factory.create_play(content_object=track)
        response = self._get_plays(*{Fields.CREATED_ON: 'sfgsf'})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
