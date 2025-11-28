from bodzify_api.model.spotify_resource.Fields import Fields as SpotifyFields
from bodzify_api.model.public_standard_resource.Fields import Fields as PublicStandardResourceFields


class Fields(SpotifyFields, PublicStandardResourceFields):
    NAME = 'name'
    POPULARITY = 'popularity'
    SPOTIFY_LINK = 'spotify_link'
    GENRES = 'genres'
    IMAGES = 'images'
