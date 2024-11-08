from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.artist.Fields import Fields as ModelFields


class ArtistManager(BaseManager):

    def get_default_ordering(self):
        return [ModelFields.NAME]
