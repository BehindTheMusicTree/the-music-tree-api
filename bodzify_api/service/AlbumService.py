
from bodzify_api.model.album.Album import Album
from bodzify_api.model.user.User import User

from bodzify_api.serializer.schema.album.detailed import AlbumDetailedSerializer
from bodzify_api.service.Service import Service


class AlbumService(Service):

    def delete(self, user: User, instance: Album):
        instance.delete_with_tracks_and_eventually_artists()
