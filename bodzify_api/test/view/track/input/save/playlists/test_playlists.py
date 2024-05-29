#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.BasePlaylist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_new_genre_then_in_new_genre_playlist_and_all_playlist(self):
        genre_name = "Rock"
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2

        criteria_playlists = CriteriaPlaylist.objects.filter(base_playlist__in=track_playlists)
        assert criteria_playlists.filter(criteria__name=genre_name).exists()

        simple_playlists = SimplePlaylist.objects.filter(base_playlist__in=track_playlists)
        assert simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

    def test_existing_genre_then_track_in_existing_playlist_and_all_playlist(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        lib_track = self.model_fixture_factory.create_lib_track(title="Love")

        data = {PUT_FIELDS.GENRE_NAME: genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        track_playlists = self.saved_lib_track.playlists.all()
        assert len(track_playlists) == 2

        genre_playlist = CriteriaPlaylist.objects.get(criteria=genre).base_playlist
        assert lib_track in genre_playlist.library_tracks.all()  # type: ignore

        all_playlist = SimplePlaylist.objects.get(name=PLAYLIST_SPECIAL_NAMES.ALL).base_playlist
        assert lib_track in all_playlist.library_tracks.all()  # type: ignore

    def test_existing_genre_with_2_successive_ascendants_then_track_in_3_existing_playlists(self):
        rock_genre_name = "Rock"
        hardrock_genre_name = "Hard rock"
        emo_genre_name = "Emo"

        rock_genre = self.model_fixture_factory.create_genre(name=rock_genre_name)

        hardrock_genre = self.model_fixture_factory.create_genre(name=hardrock_genre_name, parent=rock_genre)

        self.model_fixture_factory.create_genre(name=emo_genre_name, parent=hardrock_genre)

        lib_track = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PUT_FIELDS.GENRE_NAME: emo_genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        lib_track_playlists = self.saved_lib_track.playlists.all()
        assert len(lib_track_playlists) == 4

        lib_track_criteria_playlists = CriteriaPlaylist.objects.filter(base_playlist__in=lib_track_playlists)
        assert lib_track_criteria_playlists.filter(criteria__name=emo_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=hardrock_genre_name).exists()
        assert lib_track_criteria_playlists.filter(criteria__name=rock_genre_name).exists()

        lib_track_simple_playlists = SimplePlaylist.objects.filter(base_playlist__in=lib_track_playlists)
        assert lib_track_simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()
