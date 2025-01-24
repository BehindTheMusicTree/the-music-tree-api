from typing import Generic, TypeVar

from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from .Fields import Fields

T = TypeVar('T', bound=PublicStandardResource)


class StandardResourceManager(BaseManager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        return [Fields.CREATED_ON]
