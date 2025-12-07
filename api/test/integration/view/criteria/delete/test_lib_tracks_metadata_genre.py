
from rest_framework import status

from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.criteria.GenreTestCase import GenreTestCase
from api.utils import audio_file_metadata


class TestCase(GenreTestCase):

    def test_delete_not_root_then_uploaded_tracks_metadata_genre_updated_to_parent(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        punk = self.model_fixture_factory.create_genre(name='criteria', parent=rock)
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title='lib track first', genre=punk,
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3)

        response = self._delete_genre(uuid=punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        metadata = audio_file_metadata.get_merged_app_metadata(file=uploaded_track.track_file.file)

        assert metadata[audio_file_metadata.AppMetadataKey.GENRE_NAME] == rock.name

    def test_delete_root_then_uploaded_tracks_metadata_genre_updated_to_none(self):
        rock = self.model_fixture_factory.create_genre(name='rock')
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title='lib track first',
            genre=rock,
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3)

        metadata = audio_file_metadata.get_merged_app_metadata(file=uploaded_track.track_file.file)
        assert metadata.get(audio_file_metadata.AppMetadataKey.GENRE_NAME) is not None

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        metadata = audio_file_metadata.get_merged_app_metadata(file=uploaded_track.track_file.file)
        assert metadata.get(audio_file_metadata.AppMetadataKey.GENRE_NAME) is None
