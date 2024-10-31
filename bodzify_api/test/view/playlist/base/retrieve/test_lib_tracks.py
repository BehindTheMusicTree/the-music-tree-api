
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.utils.utils import to_camel_case
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as LibTrackPostFields
from bodzify_api.serializer.schema.track.output.simple.simple_without_album import Fields as LibTrackGetFields
from bodzify_api.serializer.schema.playlist.children.criteria.output.detailed import Fields as CriteriaPlaylistFields


class TestCase(BasePlaylistTestCase):

    def test_retrieve_then_lib_track_ordered_by_date_added_desc(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=genre_name)

        lib_track3 = self.model_fixture_factory.create_lib_track_with_file(title="Love3", genre=genre)
        lib_track2 = self.model_fixture_factory.create_lib_track_with_file(title="Love2", genre=genre)
        lib_track1 = self.model_fixture_factory.create_lib_track_with_file(title="Love1", genre=genre)

        response = self._retrieve(base_playlist_uuid=genre.criteria_playlist.base_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        result_tracks = result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS)]
        assert result_tracks[0][to_camel_case(LibTrackGetFields.TITLE)] == lib_track1.title
        assert result_tracks[1][to_camel_case(LibTrackGetFields.TITLE)] == lib_track2.title
        assert result_tracks[2][to_camel_case(LibTrackGetFields.TITLE)] == lib_track3.title

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        self.model_fixture_factory.create_lib_track_with_file(title='celine',
                                                              filename="Celinekin Park 284 sec.mp3",
                                                              genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(title='celine',
                                                              filename="tokyo drift x sean paul 152 sec.mp3",
                                                              genre=genre)

        response = self._retrieve(genre_criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.DURATION_IN_SEC)] == 284 + 152

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(title="Winter", genre=genre, archived=True)
        response = self._retrieve(genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer2", genre=genre, archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer3", genre=genre, archived=True)
        response = self._retrieve(genre.criteria_playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(CriteriaPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
