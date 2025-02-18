from rest_framework import status

from bodzify_api.test.view.play.PlayTestCase import PlayTestCase


class TestCase(PlayTestCase):

    def test_delete_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        play = self.model_fixture_factory.create_play(content=track)
        response = self._delete_play(uuid=play.uuid)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
