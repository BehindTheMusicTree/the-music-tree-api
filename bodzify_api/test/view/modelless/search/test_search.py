#!/usr/bin/env python

from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
  ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import Playlist, \
  ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria, SPECIAL_NAMES as CRITERIA_SPECIAL_NAMES
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_in_track_artist_and_album(self):
        summerlove_track = G(LibraryTrack,
                            user=self.test_user,
                            title="Summer Love",
                            duration=0)
        sum41_artist = G(Artist, user=self.test_user, name="Sum 41")
        jailesum_album = G(Album, user=self.test_user, name="J'ai le Sum")

        response = self.search("Sum")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['overall_total'] == 3
        results = response_json['results']
        title_key = TRACK_ATTRIBUTES_LABEL.TITLE
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
        assert response_json['results'] == 6
        assert response_json['overall_total'] == 2
        results = response_json['results']
        track_title_key = TRACK_ATTRIBUTES_LABEL.TITLE
        assert results[LibraryTrack.__name__][0][track_title_key] == werealltoblame_track.title
        playlistNname_key = PLAYLIST_ATTRIBUTES_LABEL.NAME
        assert results[Playlist.__name__][0][playlistNname_key] == CRITERIA_SPECIAL_NAMES.ALL

    def test_non_sensitiveness(self):
        G(Criteria,
          user=self.test_user,
          name="Rap",
          type=CRITERIA_TYPES_ID.GENRE)
        us_rap_genre = G(Criteria,
                       user=self.test_user,
                       name="US rap",
                       type=CRITERIA_TYPES_ID.GENRE)
        G(CriteriaPlaylist,
          user=self.test_user,
          type_id=CRITERIA_TYPES_ID.GENRE,
          criteria=us_rap_genre)
        
        response = self.search("Rap")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['overall_total'] == 2
        results = response_json['results']
        assert results[Playlist.__name__][0][PLAYLIST_ATTRIBUTES_LABEL.NAME] == "Rap"
        assert results[Playlist.__name__][1][PLAYLIST_ATTRIBUTES_LABEL.NAME] == "US rap"
