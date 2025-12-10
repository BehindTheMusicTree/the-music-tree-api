from typing import TYPE_CHECKING, TypeVar

from api.model.track_mixin.Fields import Fields
from api.model.track_mixin.TrackMixinManager import TrackMixinManager


if TYPE_CHECKING:
    from api.model.track_mixin.TrackMixin import TrackMixin

T = TypeVar('T', bound='TrackMixin')


class TrackMixinWithInternalNameManager(TrackMixinManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_INTERNAL]
