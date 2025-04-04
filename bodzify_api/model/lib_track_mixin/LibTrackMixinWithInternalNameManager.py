from typing import TYPE_CHECKING, TypeVar

from bodzify_api.model.uploaded_track_mixin.Fields import Fields
from bodzify_api.model.uploaded_track_mixin.LibTrackMixinManager import LibTrackMixinManager


if TYPE_CHECKING:
    from bodzify_api.model.uploaded_track_mixin.LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinWithInternalNameManager(LibTrackMixinManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]
