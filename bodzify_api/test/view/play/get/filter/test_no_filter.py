from rest_framework import status

from bodzify_api.model.play.Play import Play
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase


class TestCase(PlayTestCase):

    def test_no_filter_then_ok(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        self.model_fixture_factory.create_play(content_object=track)
        self.model_fixture_factory.create_play(content_object=track)

        saved_plays = list(Play.objects.all())

        response = self._get_plays()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
