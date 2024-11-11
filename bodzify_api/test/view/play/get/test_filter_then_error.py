from rest_framework import status

from bodzify_api.test.view.play.PlayTestCase import PlayTestCase


class TestCase(PlayTestCase):

    def test_filter_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        self.model_fixture_factory.create_play(content_object=track)
        self.model_fixture_factory.create_play(content_object=track)
        response = self._get_plays(invalid_filter='test')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
