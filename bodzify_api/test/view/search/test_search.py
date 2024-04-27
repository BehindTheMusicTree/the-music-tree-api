#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithoutTrackSerializer \
    import FIELDS as SIMPLE_PLAYLIST_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksSerializer \
    import FIELDS as CRITERIA_PLAYLIST_FIELDS
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import FIELDS as ARTIST_FIELDS
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import FIELDS as ALBUM_FIELDS
from bodzify_api.test.view.search.SearchTestCase import SearchTestCase


class TestCase(SearchTestCase):

    def test_query_in_track_artist_and_album(self):
        summerlove_track = self.model_fixture_factory.create_lib_track(title="Summer Love")
        sum41_artist = self.model_fixture_factory.create_artist(name="Sum 41")
        jailesum_album = self.model_fixture_factory.create_album(name="J'ai le Sum")

        response = self.search("Sum")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3
        title_key = LIB_TRACK_FIELDS.TITLE
        assert self.results[LibraryTrack.__name__][0][title_key] == summerlove_track.title
        assert self.results[Artist.__name__][0][ARTIST_FIELDS.NAME] == sum41_artist.name
        assert self.results[Album.__name__][0][ALBUM_FIELDS.NAME] == jailesum_album.name

    def test_the_all_string_including_a_track(self):
        werealltoblame_track = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        response = self.search("All")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        track_title_key = LIB_TRACK_FIELDS.TITLE
        assert self.results[LibraryTrack.__name__][0][track_title_key] == werealltoblame_track.title
        assert self.results[SimplePlaylist.__name__][0][SIMPLE_PLAYLIST_FIELDS.NAME] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_non_sensitiveness(self):
        rap_criteria_name = "Rap"
        self.model_fixture_factory.create_genre(name=rap_criteria_name)
        us_rap_criteria_name = "US rap"
        self.model_fixture_factory.create_genre(name=us_rap_criteria_name)

        response = self.search("Rap")
        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2
        assert self.results[CriteriaPlaylist.__name__][0][CRITERIA_PLAYLIST_FIELDS.NAME] == rap_criteria_name
        assert self.results[CriteriaPlaylist.__name__][1][CRITERIA_PLAYLIST_FIELDS.NAME] == us_rap_criteria_name
