from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields


class Fields:
    NAME_PUBLIC = AlbumFields.NAME_PUBLIC
    ALBUM_ARTIST_NAME = f'album_artist_{ArtistFields.NAME_PUBLIC}'
