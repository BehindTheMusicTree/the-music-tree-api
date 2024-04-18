#!/usr/bin/env python

from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.utils import to_camel_case
from bodzify_api.serializer.play.input.schema.endpoint.PlayPostSchemaSerializer import FIELDS


class TestCase(PlayTestCase):

    def test_extra_field_then_error(self):
        data = {'nonExistingField': 'oifjqoif'}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_multiple_values_for_content_object_uuid_then_error(self):
        playlist1_uuid = G(SimplePlaylist, playlist__user=self.test_user, name='test').playlist.uuid  # type: ignore
        playlist2_uuid = G(SimplePlaylist, playlist__user=self.test_user, name='test').playlist.uuid  # type: ignore
        data = {to_camel_case(FIELDS.CONTENT_OBJECT_UUID): [playlist1_uuid, playlist2_uuid]}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_non_existant_content_object_uuid_then_error(self):
        data = {to_camel_case(FIELDS.CONTENT_OBJECT_UUID): 'oifjqoif'}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_playlist_play(self):
        current_play_count = 42
        playlist_uuid = G(SimplePlaylist,
                          playlist__user=self.test_user,
                          name='test',
                          playlist__play_count=current_play_count).playlist.uuid  # type: ignore
        data = {to_camel_case(FIELDS.CONTENT_OBJECT_UUID): playlist_uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_play.content_object.uuid == playlist_uuid  # type: ignore
        assert self.saved_play.content_object.play_count == current_play_count + 1  # type: ignore

    def test_playlist_play_then_returns_lib_tracks(self):
        criteria = G(Criteria, user=self.test_user, name='criteria1', type=CRITERIA_TYPES_ID.GENRE)  # type: ignore
        lib_track = G(LibraryTrack, user=self.test_user, title='track', genre=criteria)
        criteria_playlist = criteria.criteria_playlist.playlist  # type: ignore
        data = {to_camel_case(FIELDS.CONTENT_OBJECT_UUID): criteria_playlist.uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_play.content_object.library_tracks.first().uuid == lib_track.uuid  # type: ignore

    def test_lib_track_play(self):
        current_play_count = 455
        lib_track_uuid = G(LibraryTrack,
                           user=self.test_user,
                           title='test',
                           play_count=current_play_count).uuid  # type: ignore
        data = {to_camel_case(FIELDS.CONTENT_OBJECT_UUID): lib_track_uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_play.content_object.uuid == lib_track_uuid  # type: ignore
        assert self.saved_play.content_object.play_count == current_play_count + 1  # type: ignore
