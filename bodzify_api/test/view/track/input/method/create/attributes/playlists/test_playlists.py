#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.BasePlaylist import SpecialNames as PLAYLIST_SPECIAL_NAMES
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_no_genre_then_in_the_all_and_genreless_playlists(self):
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED

        track_playlists = self.saved_lib_track.base_playlists.all()
        assert len(track_playlists) == 2

        track_simple_playlists = SimplePlaylist.objects.filter(base_playlist__in=track_playlists)
        assert track_simple_playlists.filter(name=PLAYLIST_SPECIAL_NAMES.ALL).exists()

        track_criteria_playlists = CriteriaPlaylist.objects.filter(base_playlist__in=track_playlists)
        assert track_criteria_playlists.filter(criteria=None).exists()
