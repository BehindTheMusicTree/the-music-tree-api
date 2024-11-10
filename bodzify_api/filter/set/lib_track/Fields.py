from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields


class Fields:
    TITLE = ModelFields.TITLE
    ARTISTS_NAME = f'{ModelFields.ARTISTS}__{ArtistFields.NAME}'
    ALBUM_NAME = f'{ModelFields.ALBUM}__{AlbumFields.NAME}'
    GENRE_NAME = f'{ModelFields.GENRE}__{CriteriaFields.NAME}'
    LANGUAGE = ModelFields.LANGUAGE
