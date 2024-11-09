from typing import Any, TYPE_CHECKING, Self

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from bodzify_api.model.criteria.children.tag.Tag import Tag


class TagManager(CriteriaManager):
    model: type['Tag']

    def create_single(self, **kwargs) -> 'Tag':
        return super().create_single(type_pk=CriteriaTypesPks.TAG, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypesPks.TAG, *args, **kwargs)
