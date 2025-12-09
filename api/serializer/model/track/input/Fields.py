from api.model.album.Fields import Fields as AlbumFields
from api.model.artist.Fields import Fields as ArtistFields
from api.model.track.Fields import Fields as ModelFields


class Fields:
    TITLE = ModelFields.TITLE
    FORCE_TITLE_GENERATION = 'force_title_generation'
    ARTISTS_NAMES = f'{ModelFields.ARTISTS}_{ArtistFields.NAME_PUBLIC}s'
    ARTISTS_NAMES_MULTIPART = f'{ARTISTS_NAMES}[]'
    ALBUM_NAME = f'{ModelFields.ALBUM}_{AlbumFields.NAME_PUBLIC}'
    ALBUM_ARTISTS_NAMES = f'{AlbumFields.ALBUM_ARTISTS}_{ArtistFields.NAME_PUBLIC}s'
    ALBUM_ARTISTS_NAMES_MULTIPART = f'{ALBUM_ARTISTS_NAMES}[]'
    TRACK_NUMBER = ModelFields.TRACK_NUMBER
    GENRE = ModelFields.GENRE
    RATING = ModelFields.RATING
    LANGUAGE = ModelFields.LANGUAGE
    ARCHIVED = ModelFields.ARCHIVED
