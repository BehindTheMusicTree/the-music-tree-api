#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_no_genre_then_in_the_all_and_genreless_playlists(self):
        response = self.post_sample_track(sample_filename="notProvided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        
        track_playlists = self.saved_track.playlists.all()
        assert len(track_playlists) == 2

        track_simple_playlists = SimplePlaylist.objects.filter(playlist__in=track_playlists)
        assert track_simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

        track_criteria_playlists = CriteriaPlaylist.objects.filter(playlist__in=track_playlists)
        assert track_criteria_playlists.filter(criteria=None).exists()
