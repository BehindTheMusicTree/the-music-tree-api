from typing import Optional, TYPE_CHECKING

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


from bodzify_api import settings
from bodzify_api.model.base.TrackablePlayCountModel import TrackablePlayCountModel
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.playlist.children.ChildPlaylist import ChildPlaylist
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class BasePlaylist(LibTrackMixin, TrackablePlayCountModel):
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()

    class Meta:
        db_table = f'{settings.APP_NAME}_base_playlist'
        verbose_name = 'Base Playlist'
        verbose_name_plural = 'Base Playlists'
        indexes = [models.Index(fields=[Fields.USER, Fields.UUID], name='base_playlist_user_uuid_idx')]

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return self.playlist_library_tracks  # type: ignore

    @property
    def object_model_class(self) -> type[ChildPlaylist]:
        model_class = self.content_type.model_class()
        if not model_class:
            raise Exception('Model class is not set')
        return model_class  # type: ignore

    @property
    def object(self) -> ChildPlaylist:
        return self.object_model_class.objects.get(user=self.user, id=self.object_pk)

    @property
    def name(self) -> Optional[str]:
        return self.object.name

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
