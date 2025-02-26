from typing import TYPE_CHECKING

from django.db.models import QuerySet

from bodzify_api.model.lib_track_mixin.Fields import Fields
from bodzify_api.model.lib_track_mixin.LibTrackMixinWithInternalNameManager import LibTrackMixinWithInternalNameManager


if TYPE_CHECKING:
    from bodzify_api.model.artist.Artist import Artist
    from bodzify_api.model.user.User import User

    from .Album import Album


class AlbumManager(LibTrackMixinWithInternalNameManager['Album']):
    model: type['Album']

    def _get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            self, user: 'User', name: str, album_artists: list) -> 'Album | None':
        album_queryset = self.filter(user=user, name=name)
        if len(album_artists) > 0:
            for album_artist in album_artists:
                album_queryset = album_queryset.filter(album_artists__in=[album_artist])
        else:
            album_queryset = album_queryset.filter(album_artists=None)

        return (self.create_instance_with_album_artists_list(user=user,
                                                             name=name,
                                                             album_artists_list=album_artists)
                if album_queryset.count() == 0 else album_queryset.first())

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]

    def create_instance_with_album_artists_list(
            self, user: 'User', name: str, album_artists_list: list['Artist']) -> 'Album':
        album: 'Album' = self.create(user=user, name=name)
        if album_artists_list:
            album.album_artists.set(album_artists_list)
        return album

    def get_album_from_name_and_album_artists_names_list_after_eventual_creations(
            self, user: 'User', name: str, album_artists_names_list: list) -> 'Album | None':
        from bodzify_api.model.artist.Artist import Artist
        if album_artists_names_list and len(album_artists_names_list):
            album_artists = [Artist.objects.get_or_create(user=user, name=artist_name)[0]
                             for artist_name in album_artists_names_list]
        else:
            album_artists = []

        return self._get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            user=user, name=name, album_artists=album_artists)

    def delete_instance(self, instance: 'Album') -> None:
        self.delete_instance_with_tracks_and_eventually_artists(instance)

    def delete_instance_with_tracks_and_eventually_artists(self, instance: 'Album'):
        from bodzify_api.model.artist.Artist import Artist
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        # Keep this deletion order for rollback tests: first delete tracks, then delete album, then delete artists

        artists_linked_to_album_and_track: list[Artist] = []
        lib_tracks: QuerySet[LibraryTrack] = instance.lib_tracks.all()
        for track in lib_tracks:
            if track.artists.exists():
                for artist in track.artists.all():
                    if artist not in artists_linked_to_album_and_track:
                        artists_linked_to_album_and_track.append(artist)
            track.delete()

        for album_artist in instance.album_artists.all():
            if album_artist not in artists_linked_to_album_and_track:
                artists_linked_to_album_and_track.append(album_artist)

        instance.delete()

        for artist in artists_linked_to_album_and_track:
            Artist.objects.delete_instance_if_nothing_linked(artist)

    def delete_instance_if_no_track_linked_with_eventual_album_artist_deletion(self, instance: 'Album'):
        from bodzify_api.model.artist.Artist import Artist
        if instance.lib_tracks.count() == 0:
            album_artists = list(instance.album_artists.all())  # Copy the list before the deletion
            instance.delete()
            for album_artist in album_artists:
                Artist.objects.delete_instance_if_nothing_linked(album_artist)
