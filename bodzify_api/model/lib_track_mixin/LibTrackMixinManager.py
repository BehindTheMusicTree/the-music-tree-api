from typing import TYPE_CHECKING, Generic, TypeVar

from django.db import models

from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from .LibTrackMixin import LibTrackMixin

T = TypeVar('T', bound='LibTrackMixin')


class LibTrackMixinManager(PublicStandardResourceManager[T], Generic[T]):

    def lib_tracks_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.get_queryset().order_by(Fields.CREATED_ON)
