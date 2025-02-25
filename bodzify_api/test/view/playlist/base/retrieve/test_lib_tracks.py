from rest_framework import status

from bodzify_api.model.lib_track_playlist_rel.Fields import     Fields as LibTrackPlaylistRelFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import     CriteriaPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.output.simple.simple_without_album import     Fields as LibTrackOutputFields
from bodzify_api.serializer.model.playlist.base.output.detailed import     Fields as PlaylistOutputFields
from bodzify_api.test.view.playlist.base.PlaylistTestCase import     PlaylistTestCase
from bodzify_api.utils import data_transformer


class TestCase(PlaylistTestCase):

    def test_retrieve_then_lib_track_ordered_by_created_on_desc(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        lib_track3 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love3", genre=genre, use_manager_for_genre_playlist_adding=True)
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love2", genre=genre, use_manager_for_genre_playlist_adding=True)
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love1", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(uuid=genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks_raw = self.result[data_transformer.to_camel_case(
            PlaylistOutputFields.LIB_TRACK_PLAYLIST_RELS_PUBLIC)]
        result_tracks_sorted = sorted(
            result_tracks_raw, key=lambda x: x[data_transformer.to_camel_case(LibTrackPlaylistRelFields.POSITION)])
        lib_track_field_name = data_transformer.to_camel_case(LibTrackPlaylistRelFields.LIB_TRACK_PUBLIC)
        assert result_tracks_sorted[0][lib_track_field_name][LibTrackOutputFields.TITLE] == lib_track1.title
        assert result_tracks_sorted[1][lib_track_field_name][LibTrackOutputFields.TITLE] == lib_track2.title
        assert result_tracks_sorted[2][lib_track_field_name][LibTrackOutputFields.TITLE] == lib_track3.title

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        self.model_fixture_factory.create_lib_track_with_file(
            title="celine",
            genre=genre,
            filename="Celinekin Park 284 sec.mp3",
            use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="celine",
            genre=genre,
            filename="tokyo drift x sean paul 152 sec.mp3",
            use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(genre_criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(PlaylistOutputFields.DURATION_IN_SEC)] == 284 + 152

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Summer", genre=genre, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Winter", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True)

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(
            PlaylistOutputFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC)] == 3

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True)
        track_archived_1 = self.model_fixture_factory.create_lib_track_with_file(
            title="Summer", genre=genre, use_manager_for_genre_playlist_adding=True)
        track_archived_2 = self.model_fixture_factory.create_lib_track_with_file(
            title="Summer2", genre=genre, use_manager_for_genre_playlist_adding=True)
        track_archived_3 = self.model_fixture_factory.create_lib_track_with_file(
            title="Summer3", genre=genre, use_manager_for_genre_playlist_adding=True)

        for track in [track_archived_1, track_archived_2, track_archived_3]:
            LibraryTrack.objects.update_instance(track, archived=True)

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(PlaylistOutputFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC)] == 3
