from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.utils import data_transformer
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album import Fields as LibTrackGetFields
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.detailed import Fields as CriteriaPlaylistFields


class TestCase(PlaylistTestCase):

    def test_retrieve_then_lib_track_ordered_by_date_added_desc(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=genre_name)

        lib_track3 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love3", genre=genre)
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love2", genre=genre)
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(
            title="Love1", genre=genre)

        response = self._retrieve_playlist(uuid=genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[data_transformer.to_camel_case(CriteriaPlaylistFields.LIB_TRACKS)]
        assert result_tracks[0][data_transformer.to_camel_case(LibTrackGetFields.TITLE)] == lib_track1.title
        assert result_tracks[1][data_transformer.to_camel_case(LibTrackGetFields.TITLE)] == lib_track2.title
        assert result_tracks[2][data_transformer.to_camel_case(LibTrackGetFields.TITLE)] == lib_track3.title

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        self.model_fixture_factory.create_lib_track_with_file(
            title="celine", genre=genre,
            filename="Celinekin Park 284 sec.mp3")
        self.model_fixture_factory.create_lib_track_with_file(
            title="celine", genre=genre,
            filename="tokyo drift x sean paul 152 sec.mp3")

        response = self._retrieve_playlist(genre_criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(CriteriaPlaylistFields.DURATION_IN_SEC)] == 284 + 152

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(
            title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Summer", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Winter", genre=genre, archived=True)
        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK

        assert self.result[data_transformer.to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(
            title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Summer", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Summer2", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Summer3", genre=genre, archived=True)
        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK

        assert self.result[data_transformer.to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
