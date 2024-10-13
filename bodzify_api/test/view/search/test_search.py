#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SpecialNames as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.album.with_only_name_and_artists import Fields as AlbumFields
from bodzify_api.serializer.artist.with_only_name import Fields as ArtistFields
from bodzify_api.serializer.playlist.children.criteria.output.without_tracks import Fields as CriteriaPlaylistFields
from bodzify_api.serializer.playlist.children.simple.output.without_tracks import Fields as SimplePlaylistFields
from bodzify_api.serializer.track.output.detailed import Fields as LibTrackGetFields
from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_query_in_track_artist_and_album(self):
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        jailesum_album = self.model_fixture_factory.create_album(name="J'ai le Sum")
        summerlove_track = self.model_fixture_factory.create_lib_track(title="Summer Love")

        response = self._search("Sum")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3
        title_key = LibTrackGetFields.TITLE
        assert self.results[LibraryTrack.__name__][0][title_key] == summerlove_track.title
        assert self.results[Artist.__name__][0][ArtistFields.NAME] == sum41_artist.name
        assert self.results[Album.__name__][0][AlbumFields.NAME] == jailesum_album.name

    def test_the_all_string_including_a_track(self):
        werealltoblame_track = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        response = self._search("All")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        track_title_key = LibTrackGetFields.TITLE
        assert self.results[LibraryTrack.__name__][0][track_title_key] == werealltoblame_track.title
        assert self.results[SimplePlaylist.__name__][0][SimplePlaylistFields.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

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
