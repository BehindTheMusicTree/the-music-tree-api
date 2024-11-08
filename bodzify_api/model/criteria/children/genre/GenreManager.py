from typing import Any, Optional, TYPE_CHECKING, Self
from django.db.models import QuerySet

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from bodzify_api.model.criteria.children.genre.Genre import Genre


class GenreManager(CriteriaManager):
    model: type['Genre']

    def create_single(self, **kwargs) -> 'Genre':
        return super().create_single(type_pk=CriteriaTypesPks.GENRE, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypesPks.GENRE, *args, **kwargs)
