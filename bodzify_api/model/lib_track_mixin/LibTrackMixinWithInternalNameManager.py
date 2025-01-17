from typing import Any, TypeVar, Generic, TYPE_CHECKING

from django.db.models import QuerySet

from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinWithInternalNameManager(PublicStandardResourceManager[T]):
    model: type[T]

    def create(self, name: str, *args: Any, **kwargs: Any) -> T:
        # Use name parameter directly, BaseManager will transform it
        return super().create(name=name, *args, **kwargs)

    def get_or_create(self, name: str, *args: Any, **kwargs: Any) -> tuple[T, bool]:
        # Use name parameter directly, BaseManager will transform it
        return super().get_or_create(name=name, *args, **kwargs)

    def update_instance(self, instance: T, name: str, *args: Any, **kwargs: Any) -> T:
        # Use name parameter directly, BaseManager will transform it
        return super().update_instance(instance, name=name, *args, **kwargs)

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]
