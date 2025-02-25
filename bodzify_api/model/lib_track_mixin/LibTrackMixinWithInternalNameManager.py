from typing import TYPE_CHECKING, TypeVar

from bodzify_api.model.lib_track_mixin.Fields import Fields
from bodzify_api.model.lib_track_mixin.LibTrackMixinManager import LibTrackMixinManager
from bodzify_api.model.utils.query.field_transform import update_name_field

if TYPE_CHECKING:
    from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinWithInternalNameManager(LibTrackMixinManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]

    def update_instance(self, instance: T, **kwargs) -> T:
        if Fields.NAME_PUBLIC in kwargs:
            update_name_field(instance, kwargs.pop(Fields.NAME_PUBLIC))

        return super().update_instance(instance, **kwargs)
