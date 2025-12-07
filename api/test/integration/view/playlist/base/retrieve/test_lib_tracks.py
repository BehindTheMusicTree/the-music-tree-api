from rest_framework import status

from api.model.uploaded_track_playlist_rel.Fields import Fields as UploadedTrackPlaylistRelFields
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.uploaded_track.output.simple.simple_without_album import Fields as UploadedTrackOutputFields
from api.serializer.model.playlist.base.output.detailed import Fields as PlaylistOutputFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.playlist.base.PlaylistTestCase import PlaylistTestCase
from api.utils import data_transformer


class TestCase(PlaylistTestCase):

    def test_retrieve_then_uploaded_track_ordered_by_created_on_desc(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        uploaded_track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love3", genre=genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love2", genre=genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love1", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(uuid=genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks_raw = self.result[data_transformer.to_camel_case(
            PlaylistOutputFields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC)]
        result_tracks_sorted = sorted(
            result_tracks_raw, key=lambda x: x[data_transformer.to_camel_case(UploadedTrackPlaylistRelFields.POSITION)])
        uploaded_track_field_name = data_transformer.to_camel_case(UploadedTrackPlaylistRelFields.UPLOADED_TRACK_PUBLIC)
        assert result_tracks_sorted[0][uploaded_track_field_name][
            UploadedTrackOutputFields.TITLE] == uploaded_track1.title
        assert result_tracks_sorted[1][uploaded_track_field_name][
            UploadedTrackOutputFields.TITLE] == uploaded_track2.title
        assert result_tracks_sorted[2][uploaded_track_field_name][
            UploadedTrackOutputFields.TITLE] == uploaded_track3.title

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="celine",
            genre=genre,
            test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_472S_WAV,
            use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="celine",
            genre=genre,
            test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_277S_MP3,
            use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(genre_criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(PlaylistOutputFields.DURATION_IN_SEC)] == 472 + 277

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Winter", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(
            PlaylistOutputFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC)] == 2

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer2", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer3", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(
            PlaylistOutputFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC)] == 2
