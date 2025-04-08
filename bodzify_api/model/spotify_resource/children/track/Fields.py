from bodzify_api.model.spotify_resource.Fields import Fields as SpotifyFields


class Fields(SpotifyFields):
    NAME = 'name'
    DURATION_MS = 'duration_ms'
    POPULARITY = 'popularity'
    SPOTIFY_LINK = 'spotify_link'
    ALBUM = 'album'
    PREVIEW_URL = 'preview_url'
    EXPLICIT = 'explicit'
    SPOTIFY_ARTISTS = 'spotify_artists'
    LAST_SYNCED_AT = 'last_synced_at'
    IS_REMOVED = 'is_removed'
