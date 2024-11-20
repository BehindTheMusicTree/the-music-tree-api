from rest_framework import status

from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.album.minimum import Fields as AlbumFields
from bodzify_api.serializer.schema.model.artist.minimum import Fields as ArtistFields
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.simple import Fields as CriteriaPlaylistFields
from bodzify_api.serializer.schema.model.lib_track.output.detailed import Fields as LibTrackGetFields
from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_query_in_track_artist_and_album(self):
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        jailesum_album = self.model_fixture_factory.create_album(name="J'ai le Sum")
        summerlove_track = self.model_fixture_factory.create_lib_track_with_file(title="Summer Love")

        response = self._search("Sum")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3
        title_key = LibTrackGetFields.TITLE
        assert self.results[LibraryTrack.__name__][0][title_key] == summerlove_track.title
        assert self.results[Artist.__name__][0][ArtistFields.NAME] == sum41_artist.name
        assert self.results[Album.__name__][0][AlbumFields.NAME] == jailesum_album.name

    def test_non_sensitiveness(self):
        rap_criteria_name = "Rap"
        self.model_fixture_factory.create_genre(name=rap_criteria_name)
        us_rap_criteria_name = "US rap"
        self.model_fixture_factory.create_genre(name=us_rap_criteria_name)

        response = self._search("Rap")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        assert self.results[CriteriaPlaylist.__name__][0][CriteriaPlaylistFields.NAME] == rap_criteria_name
        assert self.results[CriteriaPlaylist.__name__][1][CriteriaPlaylistFields.NAME] == us_rap_criteria_name
