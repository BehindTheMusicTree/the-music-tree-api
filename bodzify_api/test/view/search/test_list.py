from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.album.minimum import Fields as AlbumFields
from bodzify_api.serializer.model.artist.minimum import Fields as ArtistFields
from bodzify_api.serializer.model.playlist.children.criteria.output.simple import Fields as CriteriaPlaylistFields
from bodzify_api.serializer.model.lib_track.output.detailed import Fields as LibTrackGetFields
from bodzify_api.filtering.set.search.Fields import Fields as SearchFields
from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_query_in_track_artist_and_album_then_results(self):
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        jailesum_album = self.model_fixture_factory.create_album(name="J'ai le Sum")
        summerlove_track = self.model_fixture_factory.create_lib_track_with_file(title="Summer Love")

        response = self._search(**{SearchFields.QUERY: "Sum"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        title_key = LibTrackGetFields.TITLE
        assert self.results[LibraryTrack.__name__][0][title_key] == summerlove_track.title
        assert self.results[Artist.__name__][0][ArtistFields.NAME] == sum41_artist.name
        assert self.results[Album.__name__][0][AlbumFields.NAME] == jailesum_album.name

    def test_contains_in_another_case_then_results(self):
        rap_criteria_name = "Rap"
        self.model_fixture_factory.create_genre(name=rap_criteria_name)
        us_rap_criteria_name = "US rap"
        self.model_fixture_factory.create_genre(name=us_rap_criteria_name)

        response = self._search(**{SearchFields.QUERY: "rap"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        assert self.results[CriteriaPlaylist.__name__][0][CriteriaPlaylistFields.NAME] == rap_criteria_name
        assert self.results[CriteriaPlaylist.__name__][1][CriteriaPlaylistFields.NAME] == us_rap_criteria_name

    def test_manual_playlist_then_results(self):
        manual_playlist_foot = self.model_fixture_factory.create_manual_playlist(name='foot')
        self.model_fixture_factory.create_manual_playlist(name='cuisine')
        response = self._search(**{SearchFields.QUERY: "Foo"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[ManualPlaylist.__name__][0][CriteriaPlaylistFields.NAME] == manual_playlist_foot.name

    def test_criteria_playlist_then_results(self):
        criteria_playlist_rock = self.model_fixture_factory.create_genre(name='rock')
        self.model_fixture_factory.create_genre(name='punk')
        response = self._search(**{SearchFields.QUERY: "roC"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[CriteriaPlaylist.__name__][0][CriteriaPlaylistFields.NAME] == criteria_playlist_rock.name

    def test_album_then_results(self):
        album = self.model_fixture_factory.create_album(name='album')
        self.model_fixture_factory.create_album(name='another one')
        response = self._search(**{SearchFields.QUERY: "aLb"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[Album.__name__][0][AlbumFields.NAME] == album.name

    def test_lib_track_then_results(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        self.model_fixture_factory.create_lib_track_with_file(title='another one')
        response = self._search(**{SearchFields.QUERY: "trA"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[LibraryTrack.__name__][0][LibTrackGetFields.TITLE] == lib_track.title

    def test_artist_then_results(self):
        artist = self.model_fixture_factory.create_artist(name='artist')
        self.model_fixture_factory.create_artist(name='another one')
        response = self._search(**{SearchFields.QUERY: "Art"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[Artist.__name__][0][ArtistFields.NAME] == artist.name
