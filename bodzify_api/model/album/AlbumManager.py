from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.album.Fields import Fields as ModelFields


class AlbumManager(BaseManager):

    def get_default_ordering(self):
        return [ModelFields.NAME]
