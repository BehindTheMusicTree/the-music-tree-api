from typing import Optional

from rest_framework import status

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.play.input.schema.endpoint.post import Fields
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as LibTrackPostFields
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(PlayTestCase):

    def test_extra_field_then_error(self) -> None:
        response = self._post_play(**{'nonExistingField': 'oifjqoif'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_multiple_values_for_content_object_uuid_then_error(self) -> None:
        playlist1_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid
        playlist2_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid

        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): [playlist1_uuid, playlist2_uuid]}
        response = self._post_play(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_non_existant_content_object_uuid_then_error(self):
        response = self._post_play(**{to_camel_case(Fields.CONTENT_OBJECT_UUID): 'oifjqoif'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_playlist_play(self) -> None:
        current_play_count = 42
        db_playlist: Playlist = self.model_fixture_factory.create_manual_playlist(name='test',
                                                                                  play_count=current_play_count)

        response = self._post_play(**{to_camel_case(Fields.CONTENT_OBJECT_UUID): db_playlist.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        response_playlist: Playlist = self.saved_play.content_object  # type: ignore
        assert response_playlist.uuid == db_playlist.uuid
        assert response_playlist.play_count == current_play_count + 1

    def test_playlist_play_then_returns_lib_tracks(self) -> None:
        criteria = self.model_fixture_factory.create_genre(name='criteria1')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="track", genre=criteria, use_manager_for_genre_playlist_adding=True)

        data = {to_camel_case(Fields.CONTENT_OBJECT_UUID): criteria.criteria_playlist.uuid}
        response = self._post_play(**data)

        assert response.status_code == status.HTTP_201_CREATED
        playlist: Playlist = self.saved_play.content_object  # type: ignore
        assert playlist.lib_tracks.count() == 1
        playlist_lib_track: Optional[LibraryTrack] = playlist.lib_tracks.first()
        assert playlist_lib_track
        assert playlist_lib_track.uuid == lib_track.uuid

    def test_lib_track_play(self) -> None:
        current_play_count = 455
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title='test', play_count=current_play_count)

        response = self._post_play(**{to_camel_case(Fields.CONTENT_OBJECT_UUID): lib_track.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        saved_lib_track: LibraryTrack = self.saved_play.content_object  # type: ignore
        assert saved_lib_track.uuid == lib_track.uuid  # Compare with original UUID
        assert self.saved_play.content_object.play_count == current_play_count + 1
