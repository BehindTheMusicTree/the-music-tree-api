from typing import TypeVar, TYPE_CHECKING

from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinManager(PublicStandardResourceManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME]

    def update_instance(self, instance: T, **kwargs) -> T:
        if Fields.NAME in kwargs:
            from bodzify_api.model.utils.query.field_transform import update_name_field
            update_name_field(instance, kwargs.pop(Fields.NAME))
        return super().update_instance(instance, **kwargs)
