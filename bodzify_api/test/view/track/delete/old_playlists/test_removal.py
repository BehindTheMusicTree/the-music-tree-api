#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.playlist.BasePlaylist import \
    SpecialNames as PlaylistSpecialNames
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_remove_from_the_all_playlist(self):
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        playlist_all = SimplePlaylist.objects.get(name=PlaylistSpecialNames.ALL).base_playlist
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in playlist_all.library_tracks.all()  # type: ignore

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

        assert track not in genre1.criteria_playlist.base_playlist.library_tracks.all()  # type: ignore
        assert track not in genre2.criteria_playlist.base_playlist.library_tracks.all()  # type: ignore
        assert track not in genre3.criteria_playlist.base_playlist.library_tracks.all()  # type: ignore
