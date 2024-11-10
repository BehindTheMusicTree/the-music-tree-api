from typing import Any, TYPE_CHECKING, Self

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Tag import Tag


class TagManager(CriteriaManager):
    model: type['Tag']

    def create(self, **kwargs) -> 'Tag':
        return super().create(type_pk=CriteriaTypePks.TAG, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypePks.TAG, *args, **kwargs)
