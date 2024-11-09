from typing import Any, TYPE_CHECKING, Self

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks
from ...CriteriaPlaylistManager import CriteriaPlaylistManager

if TYPE_CHECKING:
    from .TagPlaylist import TagPlaylist


class TagPlaylistManager(CriteriaPlaylistManager):
    model: type['TagPlaylist']

    def create(self, **kwargs) -> 'TagPlaylist':
        return super().create(type_pk=CriteriaTypesPks.TAG, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypesPks.TAG, *args, **kwargs)
