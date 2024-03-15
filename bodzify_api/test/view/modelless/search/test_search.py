#!/usr/bin/env python

from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.ApiTestCase import ApiViewTestCase
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithoutTrackSerializer \
    import FIELDS as SIMPLE_PLAYLIST_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksSerializer \
    import FIELDS as CRITERIA_PLAYLIST_FIELDS
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import FIELDS as ARTIST_FIELDS
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import FIELDS as ALBUM_FIELDS


class TestCase(ApiViewTestCase):

    def test_query_in_track_artist_and_album(self):
        summerlove_track = G(LibraryTrack,
                             user=self.test_user,
                             title="Summer Love",
                             duration=0)
        sum41_artist = G(Artist, user=self.test_user, name="Sum 41")
        jailesum_album = G(Album, user=self.test_user, name="J'ai le Sum")

        response = self.search("Sum")
        assert response.status_code == 200  # type: ignore
        response_json = response.json()  # type: ignore
        assert response_json[ApiViewTestCase.RESPONSE_FIELDS.OVERALL_TOTAL] == 3
        title_key = LIB_TRACK_FIELDS.TITLE
        assert self.results[LibraryTrack.__name__][0][title_key] == summerlove_track.title  # type: ignore
        assert self.results[Artist.__name__][0][ARTIST_FIELDS.NAME] == sum41_artist.name  # type: ignore
        assert self.results[Album.__name__][0][ALBUM_FIELDS.NAME] == jailesum_album.name  # type: ignore

    def test_the_all_string_including_a_track(self):
        werealltoblame_track = G(LibraryTrack,
                                 user=self.test_user,
                                 title="We're All To Blame",
                                 duration=0)
        response = self.search("All")
        assert response.status_code == 200  # type: ignore
        response_json = response.json()  # type: ignore
        assert response_json[ApiViewTestCase.RESPONSE_FIELDS.OVERALL_TOTAL] == 2
        track_title_key = LIB_TRACK_FIELDS.TITLE
        assert self.results[LibraryTrack.__name__][0][track_title_key] == werealltoblame_track.title  # type: ignore
        simple_playlist_name_key = SIMPLE_PLAYLIST_FIELDS.NAME
        assert self.results[SimplePlaylist.__name__][0][simple_playlist_name_key] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

    def test_non_sensitiveness(self):
        rap_criteria_name = "Rap"
        G(Criteria,
          user=self.test_user,
          name=rap_criteria_name,
          type=CRITERIA_TYPES_ID.GENRE)
        us_rap_criteria_name = "US rap"
        G(Criteria,
          user=self.test_user,
          name=us_rap_criteria_name,
          type=CRITERIA_TYPES_ID.GENRE)

        response = self.search("Rap")
        assert response.status_code == 200  # type: ignore
        response_json = response.json()  # type: ignore
        assert response_json[ApiViewTestCase.RESPONSE_FIELDS.OVERALL_TOTAL] == 2
        assert self.results[CriteriaPlaylist.__name__][0][CRITERIA_PLAYLIST_FIELDS.NAME] == rap_criteria_name
        assert self.results[CriteriaPlaylist.__name__][1][CRITERIA_PLAYLIST_FIELDS.NAME] == us_rap_criteria_name
