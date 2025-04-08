from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.spotify.children.artist.Fields import Fields


class SpotifyArtistManager(StandardResourceManager):
    def get_default_ordering(self):
        return [Fields.NAME]
