#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist, SpecialNames
from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_archived_lib_track_then_simple_playlist_has_plus_1_archived_lib_tracks(self):
        simple_playlist_name = "simple playlist"
        simple_playlist = self.model_fixture_factory.create_simple_playlist(name=simple_playlist_name)
        simple_playlist_base = simple_playlist.base_playlist
        track = self.model_fixture_factory.create_lib_track(title="not archived 1")
        track.base_playlists.add(simple_playlist_base)
        track_archived = self.model_fixture_factory.create_lib_track(title="archived 1", archived=True)
        track_archived.base_playlists.add(simple_playlist_base)

        data = {PutFields.ARCHIVED: "true"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        simple_playlist_base_saved = SimplePlaylist.objects.get(name=simple_playlist_name).base_playlist
        assert simple_playlist_base_saved.lib_tracks_count_archived == 2  # type: ignore
        assert simple_playlist_base_saved.lib_tracks_count == 0  # type: ignore

    def test_archived_lib_track_then_all_playlist_has_plus_1_archived_lib_tracks(self):
        self.model_fixture_factory.create_lib_track(title="not archived 1")
        self.model_fixture_factory.create_lib_track(title="archived 1", archived=True)
        track_love = self.model_fixture_factory.create_lib_track(title="Love")
        data = {PutFields.ARCHIVED: "true"}
        response = self.put_lib_track(lib_track_uuid=track_love.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        playlist_all = SimplePlaylist.objects.get(name=SpecialNames.ALL).base_playlist
        assert playlist_all.lib_tracks_count_archived == 2  # type: ignore
        assert playlist_all.lib_tracks_count == 0  # type: ignore

    def test_archived_lib_track_then_criteria_playlist_has_plus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_lib_track(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="archived 1", archived=True, genre=criteria)
        track_love = self.model_fixture_factory.create_lib_track(title="Love", genre=criteria)
        data = {PutFields.ARCHIVED: "true"}
        response = self.put_lib_track(lib_track_uuid=track_love.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        criteria_playlist_base_saved = self.lib_track_saved.genre.criteria_playlist.base_playlist  # type: ignore
        assert criteria_playlist_base_saved.lib_tracks_count_archived == 2  # type: ignore
        assert criteria_playlist_base_saved.lib_tracks_count == 0  # type: ignore
