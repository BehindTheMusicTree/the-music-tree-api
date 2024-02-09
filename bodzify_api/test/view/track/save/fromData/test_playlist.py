#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES, Playlist
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_newGenreThenInNewGenrePlaylistAndAllPlaylist(self):
        genreName = "Rock"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.saved_track.playlists.all()
        assert len(trackPlaylists) == 2
        criteriaPlaylists = trackPlaylists.instance_of(CriteriaPlaylist)
        assert criteriaPlaylists.filter(
            criteriaplaylist__criteria__name=genreName).exists()
        simplePlaylists = trackPlaylists.instance_of(SimplePlaylist)
        assert simplePlaylists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_existingGenreThenTrackInExistingPlaylistAndAllPlaylist(self):
        genreName = "Rock"
        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genreName
        }
        self.post_genre(dataJson)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genreName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.saved_track.playlists.all()
        assert len(trackPlaylists) == 2
        criteriaPlaylists = trackPlaylists.instance_of(CriteriaPlaylist)
        assert criteriaPlaylists.filter(
            criteriaplaylist__criteria__name=genreName).exists()
        simplePlaylists = trackPlaylists.instance_of(SimplePlaylist)
        assert simplePlaylists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_existingGenreWith2SuccessiveParentsThenTrackIn3ExistingPlaylists(self):
        rockGenreName = "Rock"
        hardrockGenreName = "Hard rock"
        emoGenreName = "Emo"

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: rockGenreName
        }
        self.post_genre(dataJson)
        rockGenre = self.saved_genre

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: hardrockGenreName,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rockGenre.uuid
        }
        self.post_genre(dataJson)
        hardrockGenre = self.saved_genre

        dataJson = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: emoGenreName,
            CRITERIA_ATTRIBUTES_LABEL.PARENT: hardrockGenre.uuid
        }
        self.post_genre(dataJson)

        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: emoGenreName
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        trackPlaylists = self.saved_track.playlists.all()
        assert len(trackPlaylists) == 4
        
        criteriaPlaylists = trackPlaylists.instance_of(CriteriaPlaylist)
        assert criteriaPlaylists.filter(
            criteriaplaylist__criteria__name=emoGenreName).exists()
        assert criteriaPlaylists.filter(
            criteriaplaylist__criteria__name=hardrockGenreName).exists()
        assert criteriaPlaylists.filter(
            criteriaplaylist__criteria__name=rockGenreName).exists()
        
        simplePlaylists = trackPlaylists.instance_of(SimplePlaylist)
        assert simplePlaylists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

