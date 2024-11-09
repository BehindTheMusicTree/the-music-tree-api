from typing import Optional
from rest_framework import status
from django.db.models import QuerySet

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.play.input.schema.endpoint.post import Fields
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(PlayTestCase):

    def test_extra_field_then_error(self) -> None:
        data = {'nonExistingField': 'oifjqoif'}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_multiple_values_for_content_object_uuid_then_error(self) -> None:
        playlist1_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid
        playlist2_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid
        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): [playlist1_uuid, playlist2_uuid]}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_non_existant_content_object_uuid_then_error(self):
        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): 'oifjqoif'}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_playlist_play(self) -> None:
        current_play_count = 42
        playlist_uuid = self.model_fixture_factory.create_manual_playlist(
            name='test', play_count=current_play_count).uuid
        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): playlist_uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_play.content_object
        content_object: ManualPlaylist = self.saved_play.content_object
        assert content_object.uuid == playlist_uuid
        assert content_object.play_count == current_play_count + 1

    def test_playlist_play_then_returns_lib_tracks(self) -> None:
        criteria = self.model_fixture_factory.create_genre(name='criteria1')
        lib_track: Optional[LibraryTrack] = \
            self.model_fixture_factory.create_lib_track_with_file(title='track', genre=criteria)
        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): criteria.criteria_playlist.uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_play.content_object
        content_object: CriteriaPlaylist = self.saved_play.content_object
        lib_tracks: QuerySet[LibraryTrack] = content_object.library_tracks
        assert lib_tracks.count() == 1
        lib_track = lib_tracks.first()
        assert lib_track
        assert lib_track.uuid == lib_track.uuid

    def test_lib_track_play(self) -> None:
        current_play_count = 455
        lib_track_uuid = self.model_fixture_factory.create_lib_track_with_file(
            title='test', play_count=current_play_count).uuid
        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): lib_track_uuid}
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_play.content_object
        lib_track: LibraryTrack = self.saved_play.content_object
        assert lib_track
        assert lib_track.uuid == lib_track_uuid
        assert self.saved_play.content_object.play_count == current_play_count + 1
