
from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey


class TestCase(GenreTestCase):

    def test_delete_not_root_then_lib_tracks_metadata_genre_updated_to_parent(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='criteria', parent=rock)
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title='lib track first', genre=punk,
            test_lib_track_filename=LibTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)

        response = self._delete_genre(uuid=punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        metadata = audio_metadata.get_merged_app_metadata(file=lib_track.track_file.file)

        assert metadata[AppMetadataKey.GENRE_NAME] == rock.name

    def test_delete_root_then_lib_tracks_metadata_genre_updated_to_none(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title='lib track first',
            genre=rock,
            test_lib_track_filename=LibTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        metadata = audio_metadata.get_merged_app_metadata(file=lib_track.track_file.file)
        assert metadata.get(AppMetadataKey.GENRE_NAME) is not None

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        metadata = audio_metadata.get_merged_app_metadata(file=lib_track.track_file.file)

        assert metadata.get(AppMetadataKey.GENRE_NAME) is None
