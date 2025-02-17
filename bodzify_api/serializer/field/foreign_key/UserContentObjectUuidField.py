from uuid import UUID
from typing import Any

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField


class UserContentObjectUuidField(PrivateUuidField):
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

    def __init__(self, **kwargs):
        # Create a combined queryset for both models
        # This satisfies ForeignKeyField's requirements while allowing our custom verification
        playlist_qs = Playlist.objects.all()
        library_track_qs = LibraryTrack.objects.all()
        super().__init__(queryset=playlist_qs.union(library_track_qs), **kwargs)

    def verify_user_ownership(self, uuid_obj: UUID, user: Any) -> bool:
        """
        Custom ownership verification that checks both model types.
        Overrides the default single-model verification to check both Playlists and LibraryTracks.
        """
        return (
            Playlist.objects.filter(user=user, uuid=uuid_obj).exists() or
            LibraryTrack.objects.filter(user=user, uuid=uuid_obj).exists()
        )
