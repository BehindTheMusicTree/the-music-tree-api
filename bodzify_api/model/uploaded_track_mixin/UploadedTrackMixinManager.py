from typing import TYPE_CHECKING, TypeVar

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.uploaded_track_mixin.UploadedTrackMixin import UploadedTrackMixin

T = TypeVar('T', bound='UploadedTrackMixin')


class UploadedTrackMixinManager(StandardResourceManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_PUBLIC]
