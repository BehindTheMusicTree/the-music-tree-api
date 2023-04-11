#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypesId
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames


@pytest.mark.django_db
class PlaylistTestCase(ApiViewTestCase):

    def test_newGenreThenInNewGenrePlaylistAndAllPlaylist(self):
        genreName = "Rock"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(name=genreName).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()

    def test_existingGenreWithParentAllThenTrackInExistingPlaylistAndAllPlaylist(self):
        genreName = "Rock"
        G(Criteria, user=self.testUser, name=genreName)
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
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
        
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 3
        assert trackPlaylists.filter(name=hardrockPlaylist.name).exists()
        assert trackPlaylists.filter(name=rockPlaylist.name).exists()
        assert trackPlaylists.filter(
            name=CriteriaSpecialNames.GENRE_ALL).exists()
