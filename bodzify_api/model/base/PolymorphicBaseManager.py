from typing import TypeVar

from polymorphic.managers import PolymorphicManager

from bodzify_api.model.base.BaseManager import BaseManager


T = TypeVar('T', bound='BaseModel')  # type: ignore


class PolymorphicBaseManager(BaseManager[T], PolymorphicManager):
    """
    Manager that combines functionality of BaseManager and PolymorphicManager.
    This is used for polymorphic models to ensure proper polymorphic behavior
    while maintaining BaseManager's custom functionality.
    """
    pass