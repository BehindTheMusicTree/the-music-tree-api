from typing import Any, TYPE_CHECKING, Self

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Genre import Genre


class GenreManager(CriteriaManager):
    model: 'Genre'

    def get_or_create(self, **kwargs) -> tuple[Any, bool]:
        try:
            instance = self.get(**kwargs)
            created = False
        except self.model.DoesNotExist:
            instance = self.create(**kwargs)
            created = True
        return instance, created

    def create(self, **kwargs) -> 'Genre':
        return super().create(type_id=CriteriaTypePks.GENRE, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypePks.GENRE, *args, **kwargs)
