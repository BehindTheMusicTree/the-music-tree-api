from api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from api.model.spotify_resource.children.artist.Fields import Fields


class SpotifyArtistManager(StandardResourceManager):
    def get_default_ordering(self):
        return [Fields.NAME]
