from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.track.lib.Fields import Fields as ModelFields


class Fields:
    USER = ModelFields.USER
    TRACK_FILE_USER_FRIENDLY = ModelFields.TRACK_FILE_USER_FRIENDLY
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = ModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = ModelFields.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES = f"{ModelFields.ARTISTS}_{ArtistFields.NAME}s"
    ALBUM_NAME = f"{ModelFields.ALBUM}_{AlbumFields.NAME}"
    ALBUM_ARTISTS_NAMES = f"{ModelFields.ALBUM}_artists_{ArtistFields.NAME}s"
    POSITION_IN_ALBUM = ModelFields.POSITION_IN_ALBUM
    GENRE_UUID = f"{ModelFields.GENRE}_{CriteriaFields.UUID}"
    GENRE_NAME = f"{ModelFields.GENRE}_{CriteriaFields.NAME}"
    RATING = ModelFields.RATING
    LANGUAGE = ModelFields.LANGUAGE
    ARCHIVED = ModelFields.ARCHIVED
