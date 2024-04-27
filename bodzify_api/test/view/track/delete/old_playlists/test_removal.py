#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_remove_from_the_all_playlist(self):
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        all_playlist = SimplePlaylist.objects.get(name=PLAYLIST_SPECIAL_NAMES.ALL).playlist
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in all_playlist.library_tracks.all()  # type: ignore

    def test_delete_then_remove_from_the_genre_playlists(self):
        genre1_name = "Rock"
        genre1 = self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Hard rock"
        genre2 = self.model_fixture_factory.create_genre(name=genre2_name, parent=genre1)
        genre3_name = "Emo"
        genre3 = self.model_fixture_factory.create_genre(name=genre3_name, parent=genre2)

        track = self.model_fixture_factory.create_lib_track(title="Love", genre=genre3)

        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert track not in genre1.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre2.criteria_playlist.playlist.library_tracks.all()  # type: ignore
        assert track not in genre3.criteria_playlist.playlist.library_tracks.all()  # type: ignore
