from abc import abstractmethod
from typing import TYPE_CHECKING

from django.db import models

from api.model.private_unique_resource.PrivateUniqueResource import PrivateUniqueResource
from api.model.track.Fields import Fields as TrackFields


if TYPE_CHECKING:
    from api.model.track.Track import Track


class TrackMixin(PrivateUniqueResource):

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def tracks(self) -> models.QuerySet['Track']:
        pass

    @property
    @abstractmethod
    def tracks_not_archived(self) -> models.QuerySet['Track']:
        return self.tracks.filter(archived=False)

    @property
    def tracks_not_archived_sorted(self) -> models.QuerySet['Track']:
        return self.tracks_not_archived.order_by(f'-{TrackFields.CREATED_ON}')

    @property
    def tracks_not_archived_count(self) -> int:
        return self.tracks_not_archived.count()

    @property
    def tracks_archived_count(self) -> int:
        return self.tracks.filter(archived=True).count()

    @property
    def duration_in_sec(self) -> int:
        return 0

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        total_seconds = self.duration_in_sec
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
