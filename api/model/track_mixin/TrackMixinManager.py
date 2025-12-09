from typing import TYPE_CHECKING, TypeVar

from api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .Fields import Fields


if TYPE_CHECKING:
    from api.model.track_mixin.TrackMixin import TrackMixin

T = TypeVar('T', bound='TrackMixin')


class TrackMixinManager(StandardResourceManager[T]):
    model: type[T]

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME_PUBLIC]
