from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields


class Fields:
    NAME = AlbumFields.NAME
    ALBUM_ARTISTS_NAME = f'{AlbumFields.ALBUM_ARTISTS}__{ArtistFields.NAME}'
