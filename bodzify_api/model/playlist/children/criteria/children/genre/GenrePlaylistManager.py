from typing import Any, TYPE_CHECKING, Self

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks
from ...CriteriaPlaylistManager import CriteriaPlaylistManager

if TYPE_CHECKING:
    from .GenrePlaylist import GenrePlaylist


class GenrePlaylistManager(CriteriaPlaylistManager):
    model: type['GenrePlaylist']

    def create(self, **kwargs) -> 'GenrePlaylist':
        return super().create(type_pk=CriteriaTypesPks.GENRE, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypesPks.GENRE, *args, **kwargs)
