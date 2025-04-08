from bodzify_api.model.spotify.children.track.Fields import Fields as ModelFields
from bodzify_api.model.spotify.children.artist.Fields import Fields as ArtistFields
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class Fields(PrivateUniqueResourceFields):
    NAME_PUBLIC = ModelFields.NAME
    ALBUM_ARTIST_NAME = f'spotify_artists_{ArtistFields.NAME}'
    DURATION_SEC_MIN = f'{ModelFields.DURATION_MS}_sec_min'
    DURATION_SEC_MAX = f'{ModelFields.DURATION_MS}_sec_max'
    POPULARITY_MIN = f'{ModelFields.POPULARITY}_min'
    POPULARITY_MAX = f'{ModelFields.POPULARITY}_max'
    EXPLICIT = ModelFields.EXPLICIT
    LAST_SYNCED_AT = ModelFields.LAST_SYNCED_AT
    LAST_SYNCED_AT_GT = f'{ModelFields.LAST_SYNCED_AT}_gt'
    LAST_SYNCED_AT_LT = f'{ModelFields.LAST_SYNCED_AT}_lt'
    LAST_SYNCED_AT_GTE = f'{ModelFields.LAST_SYNCED_AT}_gte'
    LAST_SYNCED_AT_LTE = f'{ModelFields.LAST_SYNCED_AT}_lte'
    IS_REMOVED = ModelFields.IS_REMOVED
