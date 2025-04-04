from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields
from bodzify_api.model.uploaded_track.Fields import Fields as ModelFields


class Fields:
    TITLE = ModelFields.TITLE
    ARTISTS_NAME = f'{ModelFields.ARTISTS}_{ArtistFields.NAME_PUBLIC}'
    ALBUM_NAME = f'{ModelFields.ALBUM}_{AlbumFields.NAME_PUBLIC}'
    GENRE_NAME = f'{ModelFields.GENRE}_{CriteriaFields.NAME_PUBLIC}'
    LANGUAGE = ModelFields.LANGUAGE
