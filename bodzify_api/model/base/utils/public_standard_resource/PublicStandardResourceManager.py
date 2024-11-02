from typing import Generic, TypeVar

from bodzify_api.model.base.utils.base_model.BaseManager import BaseManager
from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResource import PublicStandardResource

T = TypeVar('T', bound=PublicStandardResource)


class PublicStandardResourceManager(BaseManager, Generic[T]):
    model: type[T]

    def get_default_ordering(self):
        from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResource import Fields as ModelFields
        return [ModelFields.CREATED_ON]
