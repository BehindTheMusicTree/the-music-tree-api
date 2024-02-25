#!/usr/bin/env python

from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
    LIB_TRACK_ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import RESPONSE_KEYS, ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_in_track_artist_and_album(self):
        summerlove_track = G(LibraryTrack,
                             user=self.test_user,
                             title="Summer Love",
                             duration=0)
        sum41_artist = G(Artist, user=self.test_user, name="Sum 41")
        jailesum_album = G(Album, user=self.test_user, name="J'ai le Sum")

        response = self.search("Sum")
        assert response.status_code == 200  # type: ignore
        response_json = response.json()  # type: ignore
        assert response_json[RESPONSE_KEYS.OVERALL_TOTAL] == 3
        results = response_json[RESPONSE_KEYS.RESULTS]
        title_key = LIB_TRACK_ATTRIBUTES_LABEL.TITLE
        assert results[LibraryTrack.__name__][0][title_key] == summerlove_track.title
        assert results[Artist.__name__][0][ARTIST_ATTRIBUTES_LABEL.NAME] == sum41_artist.name
        assert results[Album.__name__][0][ARTIST_ATTRIBUTES_LABEL.NAME] == jailesum_album.name

    def test_the_all_string_including_a_track(self):
        werealltoblame_track = G(LibraryTrack,
                                 user=self.test_user,
                                 title="We're All To Blame",
                                 duration=0)
        response = self.search("All")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[RESPONSE_KEYS.OVERALL_TOTAL] == 2
        results = response_json[RESPONSE_KEYS.RESULTS]
        track_title_key = LIB_TRACK_ATTRIBUTES_LABEL.TITLE
        assert results[LibraryTrack.__name__][0][track_title_key] == werealltoblame_track.title
        playlist_name_key = ATTRIBUTES_LABEL.NAME
        assert results[SimplePlaylist.__name__][0][playlist_name_key] == SIMPLE_PLAYLIST_SPECIAL_NAMES.ALL

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
        assert response.status_code == 200
        response_json = response.json()
        assert response_json[RESPONSE_KEYS.OVERALL_TOTAL] == 2
        results = response_json[RESPONSE_KEYS.RESULTS]
        assert results[CriteriaPlaylist.__name__][0][ATTRIBUTES_LABEL.NAME] == rap_criteria_name
        assert results[CriteriaPlaylist.__name__][1][ATTRIBUTES_LABEL.NAME] == us_rap_criteria_name
