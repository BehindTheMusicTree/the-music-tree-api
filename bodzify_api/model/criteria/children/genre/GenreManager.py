from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Genre import Genre


class GenreManager(CriteriaManager):
    model: 'Genre'

    def create(self, **kwargs) -> 'Genre':
        return super().create(type_id=CriteriaTypePks.GENRE, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet['Genre']:
        return super().filter(type_id=CriteriaTypePks.GENRE, *args, **kwargs)
