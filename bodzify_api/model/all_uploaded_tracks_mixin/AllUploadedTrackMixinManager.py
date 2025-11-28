from bodzify_api.model.base.BaseManager import BaseManager


class AllUploadedTrackMixinManager(BaseManager):
    def get_default_ordering(self) -> list[str]:
        return []
