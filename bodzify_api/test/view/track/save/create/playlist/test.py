#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_noGenreThenInTheAllAndGenrelessPlaylists(self):
        response = self.postSampleTrack(sampleFilename="notProvided.mp3", dataJson={})
        assert response.status_code == status.HTTP_201_CREATED
        
        trackPlaylists = self.savedTrack.playlists.all()
        assert len(trackPlaylists) == 2
        assert trackPlaylists.filter(
            name=PLAYLIST_SPECIAL_NAMES.ALL).exists()
        assert trackPlaylists.filter(
            name=PLAYLIST_SPECIAL_NAMES.GENRE_GENRELESS).exists()
