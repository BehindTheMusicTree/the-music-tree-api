from typing import TYPE_CHECKING

from django.db import transaction

from bodzify_api.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields
from bodzify_api.model.uploaded_track_mixin.UploadedTrackMixinWithInternalNameManager import UploadedTrackMixinWithInternalNameManager


if TYPE_CHECKING:
    from bodzify_api.model.user.User import User

    from .Artist import Artist


class ArtistManager(UploadedTrackMixinWithInternalNameManager['Artist']):
    model: type['Artist']

    def get_default_ordering(self) -> list[str]:
        return [UploadedTrackMixinFields.NAME_INTERNAL]

    def get_artists_list_from_names_after_potential_creation(
            self, user: 'User', artists_names: list[str] | None) -> list['Artist']:
        return [self.get_or_create(user=user, name=artist_name)[0] for artist_name in artists_names] \
            if artists_names and len(artists_names) > 0 else []

    def delete_instance(self, instance: 'Artist'):
        with transaction.atomic():
            self.delete_instance_with_albums_and_tracks(instance)

    def delete_instance_with_albums_and_tracks(self, instance: 'Artist') -> tuple[int, dict[str, int]]:
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack

        # Keep deletion order for rollback tests

        for album in instance.albums.all():
            Album.objects.delete_instance_with_tracks_and_potentially_artists(album)

        for uploaded_track in instance.uploaded_tracks.all():
            UploadedTrack.objects.delete_instance_with_checking_album_and_artists_potential_deletion(uploaded_track)

        return instance.delete()

    def delete_instance_if_nothing_linked(self, instance: 'Artist') -> tuple[int, dict[str, int]]:
        if instance.albums.count() == 0:
            if instance.uploaded_tracks.count() == 0:
                return instance.delete()
        return 0, {}
