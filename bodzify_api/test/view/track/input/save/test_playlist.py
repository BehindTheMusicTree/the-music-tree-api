#!/usr/bin/env python

import pytest
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_new_genre_then_in_new_genre_playlist_and_all_playlist(self):
        genre_name = "Rock"
        lib_track = G(LibraryTrack, user=self.test_user, title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2

        criteria_playlists = CriteriaPlaylist.objects.filter(playlist__in=track_playlists)
        assert criteria_playlists.filter(criteria__name=genre_name).exists()

        simple_playlists = SimplePlaylist.objects.filter(playlist__in=track_playlists)
        assert simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = G(Criteria, name="Metal", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        new_genre_name = "Rock"
        lib_track = G(LibraryTrack, user=self.test_user, title="Love", genre=old_genre)
        data = {PUT_FIELDS.GENRE_NAME: new_genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        old_genre_playlist = CriteriaPlaylist.objects.get(criteria=old_genre).playlist
        assert lib_track not in old_genre_playlist.library_tracks.all()  # type: ignore

    def test_existing_genre_then_track_in_existing_playlist_and_all_playlist(self):
        genre_name = "Rock"
        genre = G(Criteria, name=genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track = G(LibraryTrack, user=self.test_user, title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2

        genre_playlist = CriteriaPlaylist.objects.get(criteria=genre).playlist
        assert lib_track in genre_playlist.library_tracks.all()  # type: ignore

        all_playlist = SimplePlaylist.objects.get(playlist__user=self.test_user,
                                                  name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        assert lib_track in all_playlist.library_tracks.all()  # type: ignore

    def test_existing_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        rock_genre = G(Criteria, name=rock_genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)

        hardrock_genre = G(Criteria,
                           name=hardrock_genre_name,
                           user=self.test_user,
                           type=CRITERIA_TYPES_ID.GENRE,
                           parent=rock_genre)

        G(Criteria, name=emo_genre_name, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=hardrock_genre)

        lib_track = G(LibraryTrack, user=self.test_user, title="Love")
        data = {PUT_FIELDS.GENRE_NAME: emo_genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        lib_track_playlists = self.saved_lib_track.playlists.all()
        assert len(lib_track_playlists) == 4

        lib_track_criteria_playlists = CriteriaPlaylist.objects.filter(playlist__in=lib_track_playlists)
        assert lib_track_criteria_playlists.filter(criteria__name=emo_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=hardrock_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=rock_genre_name).exists()

        lib_track_simple_playlists = SimplePlaylist.objects.filter(playlist__in=lib_track_playlists)
        assert lib_track_simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()
