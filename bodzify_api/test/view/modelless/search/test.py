#!/usr/bin/env python
from ddf import G
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
  ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import Playlist, \
  ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.PlaylistType import PlaylistTypesId
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesId
from bodzify_api.test.view.ViewTestCase import ViewTestCase
from django.urls import reverse


class SearchViewTestCase(ViewTestCase):

    def _search(self, query):
        return self.apiClient.get(path=reverse('search-list'), data={'query': query})

    def test_inTrackArtistAndAlbum(self):
        summerloveTrack = G(LibraryTrack,
                            user=self.testUser,
                            title="Summer Love",
                            duration=0)
        sum41Artist = G(Artist, user=self.testUser, name="Sum 41")
        jailesumAlbum = G(Album, user=self.testUser, name="J'ai le Sum")

        response = self._search("Sum")
        assert response.status_code == 200
        responseJson = response.json()
        assert responseJson['overall_total'] == 3
        results = responseJson['results']
        titleKey = TRACK_ATTRIBUTES_LABEL.TITLE
        assert results[LibraryTrack.__name__][0][titleKey] == summerloveTrack.title
        assert results[Artist.__name__][0][Artist.ATTRIBUTE_NAME_LABEL] == sum41Artist.name
        assert results[Album.__name__][0][Album.ATTRIBUTE_NAME_LABEL] == jailesumAlbum.name

    def test_theAllStringIncludingATrack(self):
        werealltoblameTrack = G(LibraryTrack,
                                user=self.testUser,
                                title="We're All To Blame",
                                duration=0)
        response = self._search("All")
        assert response.status_code == 200
        responseJson = response.json()
        assert responseJson['overall_total'] == 2
        results = responseJson['results']
        trackTitleKey = TRACK_ATTRIBUTES_LABEL.TITLE
        assert results[LibraryTrack.__name__][0][trackTitleKey] == werealltoblameTrack.title
        playlistNameKey = PLAYLIST_ATTRIBUTES_LABEL.NAME
        assert results[Playlist.__name__][0][playlistNameKey] == CriteriaSpecialNames.GENRE_ALL

    def test_nonSensitiveness(self):
        rapGenre = G(Criteria,
                     user=self.testUser,
                     name="Rap",
                     type_id=CriteriaTypesId.GENRE)
        G(CriteriaPlaylist,
          user=self.testUser,
          type_id=CriteriaTypesId.GENRE,
          criteria=rapGenre)
        usRapGenre = G(Criteria,
                       user=self.testUser,
                       name="US rap",
                       type_id=CriteriaTypesId.GENRE)
        G(CriteriaPlaylist,
          user=self.testUser,
          type_id=CriteriaTypesId.GENRE,
          criteria=usRapGenre)
        
        response = self._search("Rap")
        assert response.status_code == 200
        responseJson = response.json()
        assert responseJson['overall_total'] == 2
        results = responseJson['results']
        assert results[Playlist.__name__][0][PLAYLIST_ATTRIBUTES_LABEL.NAME] == "Rap"
        assert results[Playlist.__name__][1][PLAYLIST_ATTRIBUTES_LABEL.NAME] == "US rap"
