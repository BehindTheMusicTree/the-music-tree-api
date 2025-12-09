from rest_framework import status

from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_not_root_then_tracks_related_are_now_related_to_parent(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='criteria', parent=rock)
        track_first = self.model_fixture_factory.create_track_with_file(
            title='lib track first', genre=punk)
        track_second = self.model_fixture_factory.create_track_with_file(
            title='lib track second', genre=punk)

        response = self._delete_genre(uuid=punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        track_first.refresh_from_db()
        assert track_first.genre == rock

        track_second.refresh_from_db()
        assert track_second.genre == rock

    def test_delete_root_then_tracks_related_have_no_genre(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        track_first = self.model_fixture_factory.create_track_with_file(
            title='lib track first', genre=rock)
        track_second = self.model_fixture_factory.create_track_with_file(
            title='lib track second', genre=rock)

        response = self._delete_genre(uuid=rock.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        track_first.refresh_from_db()
        assert track_first.genre is None

        track_second.refresh_from_db()
        assert track_second.genre is None
