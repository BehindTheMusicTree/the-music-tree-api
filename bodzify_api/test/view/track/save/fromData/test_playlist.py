#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypesId
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames


@pytest.mark.django_db
class PlaylistTestCase(ApiViewTestCase):

    def test_noGenreThenInTheAllAndGenrelessPlaylists(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_GENRELESS).exists()

    def test_newGenreThenInNewGenrePlaylistAndAllPlaylist(self):
        genreName = "Rock"
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(name=genreName).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()

    def test_existingGenreWithParentAllThenTrackInExistingPlaylistAndAllPlaylist(self):
        genreName = "Rock"
        G(Criteria, user=self.testUser, name=genreName)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(name=genreName).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()

        genrePlaylist = trackPlaylists.get(name=genreName)
        assert genrePlaylist.parent.name == CriteriaSpecialNames.GENRE_ALL

    def test_existingGenreWith2ParentsThenTrackIn3ExistingPlaylists(self):
        genreName = "Hard rock"
        
        rockGenre = G(Criteria, user=self.testUser, name="Rock")
        hardrockGenre = G(Criteria, user=self.testUser,
                          name=genreName, parent=rockGenre)

        rockPlaylist = G(Playlist, user=self.testUser,
                         type=PlaylistTypesId.GENRE, criteria=rockGenre)
        hardrockPlaylist = G(Playlist, user=self.testUser,
                         type=PlaylistTypesId.GENRE, criteria=hardrockGenre)
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "genreName": genreName,
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 3
        assert trackPlaylists.filter(name=hardrockPlaylist.name).exists()
        assert trackPlaylists.filter(name=rockPlaylist.name).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()
