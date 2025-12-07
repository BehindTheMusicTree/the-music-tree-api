from typing import TYPE_CHECKING, TypeVar

from api.model.uploaded_track_mixin.Fields import Fields
from api.model.uploaded_track_mixin.UploadedTrackMixinManager import UploadedTrackMixinManager


if TYPE_CHECKING:
    from api.model.uploaded_track_mixin.UploadedTrackMixin import UploadedTrackMixin

T = TypeVar('T', bound='UploadedTrackMixin')


class UploadedTrackMixinWithInternalNameManager(UploadedTrackMixinManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]
