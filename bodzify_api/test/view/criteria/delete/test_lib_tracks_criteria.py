from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_not_root_then_lib_tracks_related_are_now_related_to_parent(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='criteria', parent=rock)
        lib_track_first = self.model_fixture_factory.create_lib_track_with_file(name='lib track first', genre=punk)
        lib_track_second = self.model_fixture_factory.create_lib_track_with_file(name='lib track second', genre=punk)

        response = self._delete_genre(uuid=punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        lib_track_first.refresh_from_db()
        assert lib_track_first.genre == rock

        lib_track_second.refresh_from_db()
        assert lib_track_second.genre == rock

    def test_delete_root_then_lib_tracks_related_have_no_genre(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        lib_track_first = self.model_fixture_factory.create_lib_track_with_file(name='lib track first', genre=rock)
        lib_track_second = self.model_fixture_factory.create_lib_track_with_file(name='lib track second', genre=rock)

        response = self._delete_genre(uuid=rock.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        lib_track_first.refresh_from_db()
        assert lib_track_first.genre is None

        lib_track_second.refresh_from_db()
        assert lib_track_second.genre is None
