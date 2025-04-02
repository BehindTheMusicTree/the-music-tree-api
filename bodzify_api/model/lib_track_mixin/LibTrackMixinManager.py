from typing import TYPE_CHECKING, TypeVar

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinManager(StandardResourceManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_PUBLIC]
