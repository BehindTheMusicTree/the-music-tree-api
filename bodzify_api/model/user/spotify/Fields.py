from bodzify_api.model.spotify.Fields import Fields as SpotifyFields
from bodzify_api.model.user.Fields import Fields as UserFields


class Fields(SpotifyFields, UserFields):
    SPOTIFY_ACCESS_TOKEN: str = "spotify_access_token"
    SPOTIFY_REFRESH_TOKEN: str = "spotify_refresh_token"
    SPOTIFY_PROFILE: str = "spotify_profile"
    SPOTIFY_TOKEN_EXPIRES_AT: str = "spotify_token_expires_at"
    SPOTIFY_TOKEN_SCOPE: str = "spotify_token_scope"
    SPOTIFY_LIBRARY_LAST_SYNCED_AT: str = "spotify_library_last_synced_at"
    SPOTIFY_SYNC_IN_PROGRESS: str = "spotify_sync_in_progress"
    EMAIL = "email"
    DISPLAY_NAME = "display_name"
    COUNTRY = "country"
    PRODUCT = "product"
    IMAGES = "images"
    URL = "url"
