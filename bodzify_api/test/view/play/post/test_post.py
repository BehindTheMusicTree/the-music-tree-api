from typing import Optional

from rest_framework import status

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.play.input.schema.PostFields import Fields
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(PlayTestCase):

    def test_extra_field_then_error(self) -> None:
        response = self._post_play(**{'nonExistingField': 'oifjqoif'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == 'nonExistingField'
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNKNOWN_FIELD.value

    def test_multiple_values_for_content_then_error(self) -> None:
        playlist1_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid
        playlist2_uuid = self.model_fixture_factory.create_manual_playlist(name='test').uuid

        data = {to_camel_case(Fields.CONTENT): [playlist1_uuid, playlist2_uuid]}
        response = self._post_play(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(Fields.CONTENT)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNEXPECTED_LIST.value

    def test_non_existant_content_then_error(self):
        response = self._post_play(**{to_camel_case(Fields.CONTENT): '88978e5e-5238-442b-bd24-dbbde478e090'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(Fields.CONTENT)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_REFERENCE.value

    def test_playlist_play(self) -> None:
        current_play_count = 42
        playlist_before_update: Playlist = self.model_fixture_factory.create_manual_playlist(
            name='test', play_count=current_play_count)

        response = self._post_play(**{to_camel_case(Fields.CONTENT): playlist_before_update.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.content.uuid == playlist_before_update.uuid
        assert self.saved_object.content.play_count == current_play_count + 1

    def test_playlist_play_then_returns_lib_tracks(self) -> None:
        criteria = self.model_fixture_factory.create_genre(name='criteria1')
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            title="track", genre=criteria, use_manager_for_genre_playlist_adding=True)

        data = {to_camel_case(Fields.CONTENT): criteria.criteria_playlist.uuid}
        response = self._post_play(**data)

        assert response.status_code == status.HTTP_201_CREATED
        playlist: Playlist = self.saved_object.content  # type: ignore
        assert playlist.lib_tracks.count() == 1
        playlist_lib_track: Optional[LibraryTrack] = playlist.lib_tracks.first()
        assert playlist_lib_track
        assert playlist_lib_track.uuid == lib_track.uuid

    def test_lib_track_play(self) -> None:
        current_play_count = 455
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title='test', play_count=current_play_count)

        response = self._post_play(**{to_camel_case(Fields.CONTENT): lib_track.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.content.uuid == lib_track.uuid
        assert self.saved_object.content.play_count == current_play_count + 1
