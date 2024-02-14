#!/usr/bin/env python
import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES, Playlist
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, Criteria
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_new_genre_then_in_new_genre_playlist_and_all_playlist(self):
        genre_name = "Rock"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_track.playlists.all()
        assert len(track_playlists) == 2
        criteria_playlists = track_playlists.instance_of(CriteriaPlaylist)
        assert criteria_playlists.filter(
            criteriaplaylist__criteria__name=genre_name).exists()
        simple_playlists = track_playlists.instance_of(SimplePlaylist)
        assert simple_playlists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = G(Criteria,
            name="Metal",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        new_genre_name = "Rock"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0,
                  genre=old_genre)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: new_genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert track not in old_genre_playlist.librarytrack_set.all()

    def test_existing_genre_then_track_in_existing_playlist_and_all_playlist(self):
        genre_name = "Rock"
        data_json = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genre_name
        }
        self.post_genre(data_json)
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)

        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_track.playlists.all()
        assert len(track_playlists) == 2
        criteria_playlists = track_playlists.instance_of(CriteriaPlaylist)
        assert criteria_playlists.filter(
            criteriaplaylist__criteria__name=genre_name).exists()
        simple_playlists = track_playlists.instance_of(SimplePlaylist)
        assert simple_playlists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_existing_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        rock_genre = G(Criteria,
            name=rock_genre_name,
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        
        hardrock_genre = G(Criteria,
            name=hardrock_genre_name,
            user=self.test_user,
            type=CriteriaTypesId.GENRE,
            parent=rock_genre)
        
        G(Criteria,
            name=emo_genre_name,
            user=self.test_user,
            type=CriteriaTypesId.GENRE,
            parent=hardrock_genre)

        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Love",
                  duration=0)
        data = {
            TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME: emo_genre_name
        }
        response = self.put_sample_track(track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_track.playlists.all()
        assert len(track_playlists) == 4
        
        criteria_playlists = track_playlists.instance_of(CriteriaPlaylist)
        assert criteria_playlists.filter(
            criteriaplaylist__criteria__name=emo_genre_name).exists()
        assert criteria_playlists.filter(
            criteriaplaylist__criteria__name=hardrock_genre_name).exists()
        assert criteria_playlists.filter(
            criteriaplaylist__criteria__name=rock_genre_name).exists()
        
        simple_playlists = track_playlists.instance_of(SimplePlaylist)
        assert simple_playlists.filter(
            simpleplaylist__name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

