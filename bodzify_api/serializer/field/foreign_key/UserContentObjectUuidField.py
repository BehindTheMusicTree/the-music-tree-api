from uuid import UUID
from typing import Any, Dict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from rest_framework.request import Request

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

from bodzify_api.model.ContentObjectFields import ContentObjectFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField


class PrivateContentUuidField(PrivateUuidField):
    """
    Special case of UserOwnedUuidField that allows references to either Playlists or LibraryTracks.
    Used when a field can accept either type of user content.

    This field is used when:
    1. The UUID could point to either a Playlist or LibraryTrack
    2. Both model types are treated as valid options
    3. The referenced object must belong to the current user

    Example:
        class PlaySerializer(serializers.ModelSerializer):
            content = UserContentObjectUuidField()  # Can reference either model type
    """

    default_error_messages = {
        'invalid': 'Invalid UUID format.',
        'does_not_exist': 'Object with this UUID does not exist.',
        'no_request': 'Request context is required.',
    }

    def __init__(self, **kwargs):
        # Set read_only=False since we handle writes
        kwargs['read_only'] = False
        super().__init__(**kwargs)
        # Initialize content type cache as None
        self._playlist_ct = None
        self._lib_track_ct = None

    def _get_playlist_ct(self):
        if self._playlist_ct is None:
            self._playlist_ct = ContentType.objects.get_for_model(Playlist)
        return self._playlist_ct

    def _get_lib_track_ct(self):
        if self._lib_track_ct is None:
            self._lib_track_ct = ContentType.objects.get_for_model(LibraryTrack)
        return self._lib_track_ct

    def get_queryset(self):
        user = self.get_request_user()
        return (
            Playlist.objects.filter(user=user) |
            LibraryTrack.objects.filter(user=user)
        )

    def get_request_user(self) -> Any:
        request = self.context.get('request')
        if not isinstance(request, Request):
            raise ImproperlyConfigured("request must be a Request instance.")
        return request.user

    def to_representation(self, obj: Any) -> str:
        return str(obj.uuid) if obj else ''

    def fail(self, key: str, **kwargs: Any) -> None:
        """
        Raise an AppValidationError with appropriate error code and message.

        Args:
            key: The error key that maps to an error message
            **kwargs: Format parameters for the error message
        """
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Invalid input for {class_name}."

        if key == 'invalid':
            code = FieldValidationErrorCode.INVALID_FORMAT
        elif key == 'does_not_exist':
            code = FieldValidationErrorCode.INVALID_REFERENCE
        else:
            code = FieldValidationErrorCode.DEFAULT

        raise AppValidationError(field=self.get_error_field_name(), message=msg, field_validation_error_code=code)

    def to_internal_value(self, data: Any) -> Dict[str, Any]:
        if data is None:
            return {ContentObjectFields.CONTENT_TYPE: None, ContentObjectFields.CONTENT: None}

        try:
            uuid = UUID(str(data))
        except (ValueError, AttributeError, TypeError):
            self.fail('invalid')
            return {}  # Never reached due to fail()

        user = self.get_request_user()

        # Check both models for the UUID, ensuring user ownership and get the actual object
        playlist = Playlist.objects.filter(user=user, uuid=uuid).first()
        if playlist:
            return {
                ContentObjectFields.CONTENT_TYPE: self._get_playlist_ct(),
                ContentObjectFields.CONTENT: playlist
            }

        lib_track = LibraryTrack.objects.filter(user=user, uuid=uuid).first()
        if lib_track:
            return {
                ContentObjectFields.CONTENT_TYPE: self._get_lib_track_ct(),
                ContentObjectFields.CONTENT: lib_track
            }
        self.fail('does_not_exist')

        return {}  # Never reached due to fail()
