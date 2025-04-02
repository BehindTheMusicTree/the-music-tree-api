from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.track.lib.Fields import Fields as ModelFields


class InputFields:
    TRACK_FILE_INTERNAL = ModelFields.TRACK_FILE_INTERNAL
    TRACK_FILE_PUBLIC = ModelFields.TRACK_FILE_PUBLIC
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = ModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
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
