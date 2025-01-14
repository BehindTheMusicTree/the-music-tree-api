from typing import TYPE_CHECKING, Any, List, Optional

from django.db.models import QuerySet

from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.artist.Artist import Artist
    from .Album import Album


class AlbumManager(PublicStandardResourceManager):
    model: 'Album'

    def _get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            self, user: 'User', name: str, album_artists: list) -> Optional['Album']:
        album_queryset = self.filter(user=user, name=name)
        if len(album_artists) > 0:
            for album_artist in album_artists:
                album_queryset = album_queryset.filter(album_artists__in=[album_artist])
        else:
            album_queryset = album_queryset.filter(album_artists=None)

        return self.create_instance_with_album_artists_list(user=user,
                                                            name=name,
                                                            album_artists_list=album_artists) \
            if album_queryset.count() == 0 else album_queryset.first()

    def create(self, name: str, *args: Any, **kwargs: Any) -> 'Album':
        return super().create(_name=name, *args, **kwargs)

    def update_instance(self, instance: 'Album', name: str, *args: Any, **kwargs: Any) -> 'Album':
        return super().update_instance(instance, _name=name, *args, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet['Album']:
        if Fields.NAME in kwargs:
            kwargs[Fields.NAME_INTERNAL] = kwargs[Fields.NAME]
            del kwargs[Fields.NAME]
        return super().filter(*args, **kwargs)

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]

    def create_instance_with_album_artists_list(
            self, user: 'User', name: str, album_artists_list: list['Artist']) -> 'Album':
        album: Album = self.create(user=user, name=name)
        if album_artists_list:
            album.album_artists.set(album_artists_list)
        return album

    def get_album_from_name_and_album_artists_names_list_after_eventual_creations(
            self, user: 'User', name: str, album_artists_names_list: list) -> Optional['Album']:
        from bodzify_api.model.artist.Artist import Artist
        album_artists = [Artist.objects.get_or_create(user=user, _name=artist_name)[0]
                         for artist_name in album_artists_names_list] if album_artists_names_list and len(
            album_artists_names_list) > 0 else []

        return self._get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            user=user, name=name, album_artists=album_artists)

    def delete_instance(self, instance: 'Album') -> None:
        self.delete_instance_with_tracks_and_eventually_artists(instance)

    def delete_instance_with_tracks_and_eventually_artists(self, instance: 'Album'):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        from bodzify_api.model.artist.Artist import Artist

        # Keep this deletion order for rollback tests: first delete tracks, then delete album, then delete artists

        artists_linked_to_album_and_track: List[Artist] = []
        lib_tracks: QuerySet[LibraryTrack] = instance.library_tracks.all()
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
        if instance.library_tracks.count() == 0:
            album_artists = instance.album_artists.all()
            instance.delete()
            for album_artist in album_artists:
                Artist.objects.delete_instance_if_nothing_linked(album_artist)
