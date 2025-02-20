from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.Fields import Fields as CriteriaFields


class Fields:
    TRACK_FILE_PUBLIC = ModelFields.TRACK_FILE_PUBLIC
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = ModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = ModelFields.TITLE
    FORCE_TITLE_GENERATION = 'force_title_generation'
    ARTISTS_NAMES = f'{ModelFields.ARTISTS}_{ArtistFields.NAME}s'
    ARTISTS_NAMES_ARRAY = f'{ARTISTS_NAMES}[]'
    ALBUM_NAME = f'{ModelFields.ALBUM}_{AlbumFields.NAME}'
    ALBUM_ARTISTS_NAMES = f'{AlbumFields.ALBUM_ARTISTS}_{ArtistFields.NAME}s'
    ALBUM_ARTISTS_NAMES_ARRAY = f'{ALBUM_ARTISTS_NAMES}[]'
    POSITION_IN_ALBUM = ModelFields.POSITION_IN_ALBUM
    GENRE_UUID = f'{ModelFields.GENRE}_{CriteriaFields.UUID}'
    GENRE_NAME = f'{ModelFields.GENRE}_{CriteriaFields.NAME_PUBLIC}'
    RATING = ModelFields.RATING
    LANGUAGE = ModelFields.LANGUAGE
    ARCHIVED = ModelFields.ARCHIVED
