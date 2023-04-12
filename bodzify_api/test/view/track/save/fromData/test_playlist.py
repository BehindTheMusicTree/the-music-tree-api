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
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


@pytest.mark.django_db
class PlaylistTestCase(ApiViewTestCase):

    def test_newGenreThenInNewGenrePlaylistAndAllPlaylist(self):
        genreName = "Rock"
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(criteria__name=genreName).exists()
        assert trackPlaylists.filter(
            criteria__name=CriteriaSpecialNames.GENRE_ALL).exists()

    def test_existingGenreWithParentAllThenTrackInExistingPlaylistAndAllPlaylist(self):
        genreName = "Rock"
        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genreName
        }
        self.postGenre(dataJson)
        rockGenre = self.savedGenre
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(criteria=rockGenre).exists()
        assert trackPlaylists.filter(
            criteria__name=CriteriaSpecialNames.GENRE_ALL).exists()

        genrePlaylist = trackPlaylists.get(criteria=rockGenre)
        assert genrePlaylist.parent.name == CriteriaSpecialNames.GENRE_ALL

    def test_existingGenreWith2ParentsThenTrackIn3ExistingPlaylists(self):
        genreName = "Hard rock"

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        self.postGenre(dataJson)
        rockGenre = self.savedGenre
        rockPlaylist = Playlist.objects.get(criteria=rockGenre)
        
        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genreName,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rockGenre.uuid
        }
        self.postGenre(dataJson)
        hardrockGenre = self.savedGenre
        hardrockPlaylist = Playlist.objects.get(criteria=hardrockGenre)

        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.putSampleTrack(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 3
        assert trackPlaylists.filter(
            criteria__name=hardrockPlaylist.name).exists()
        assert trackPlaylists.filter(criteria__name=rockPlaylist.name).exists()
        assert trackPlaylists.filter(
            criteria__name=CriteriaSpecialNames.GENRE_ALL).exists()
