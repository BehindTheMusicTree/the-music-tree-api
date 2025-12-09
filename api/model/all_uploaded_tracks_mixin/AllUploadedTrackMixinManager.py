from api.model.base.BaseManager import BaseManager


class AllTrackMixinManager(BaseManager):
    def get_default_ordering(self) -> list[str]:
        return []
