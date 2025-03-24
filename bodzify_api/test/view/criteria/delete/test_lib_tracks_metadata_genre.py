
from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(GenreTestCase):

    def test_delete_not_root_then_lib_tracks_metadata_genre_updated_to_parent(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='criteria', parent=rock)
        self.model_fixture_factory.create_lib_track_with_file(name='lib track first', genre=punk)

        response = self._delete_genre(uuid=punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.saved_lib_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] == rock.name

    def test_delete_root_then_lib_tracks_metadata_genre_updated_to_none(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(name='lib track first', genre=rock)

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.saved_lib_track_metadata_with_raw_rating[AppMetadataKey.GENRE_NAME] is None
