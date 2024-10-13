#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.model.playlist.BasePlaylist import \
    SpecialNames as PlaylistSpecialNames
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_update_the_all_playlist_last_track_update_date(self):
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame")
        playlist_all = SimplePlaylist.objects.get(name=PlaylistSpecialNames.ALL).base_playlist
        last_track_list_update_date_before_deletion = playlist_all.last_track_list_update_date
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        playlist_all.refresh_from_db()
        assert playlist_all.last_track_list_update_date > last_track_list_update_date_before_deletion

    def test_delete_then_update_genre_playlist_last_track_update_date(self):
        genre = self.model_fixture_factory.create_genre(name='rock')
        genre_playlist = genre.criteria_playlist.base_playlist  # type: ignore
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame", genre=genre)
        genre_playlist_last_track_list_update_date_before_deletion = (genre_playlist.last_track_list_update_date)
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        genre_playlist.refresh_from_db()
        assert genre_playlist.last_track_list_update_date > genre_playlist_last_track_list_update_date_before_deletion

    def test_delete_then_update_parent_of_parent_of_genre_playlist_last_track_update_date(self):
        genre1 = self.model_fixture_factory.create_genre(name='rock')
        genre2 = self.model_fixture_factory.create_genre(name='punk', parent=genre1)
        genre3 = self.model_fixture_factory.create_genre(name='punk hardcore', parent=genre2)

        genre1_playlist = genre1.criteria_playlist.base_playlist  # type: ignore
        track = self.model_fixture_factory.create_lib_track(title="We're All To Blame", genre=genre3)
        genre1_playlist_last_track_list_update_date_before_deletion = genre1_playlist.last_track_list_update_date
        response = self.delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        genre1_playlist.refresh_from_db()
        assert genre1_playlist.last_track_list_update_date > genre1_playlist_last_track_list_update_date_before_deletion
