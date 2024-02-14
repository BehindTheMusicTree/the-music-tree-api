#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_noGenreThenInTheAllAndGenrelessPlaylists(self):
        response = self.post_sample_track(sample_filename="notProvided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        
        track_playlists = self.saved_track.playlists.all()
        assert len(track_playlists) == 2
        assert track_playlists.filter(
            name=PLAYLIST_SPECIAL_NAMES.ALL).exists()
        assert track_playlists.filter(
            name=PLAYLIST_SPECIAL_NAMES.GENRE_GENRELESS).exists()
