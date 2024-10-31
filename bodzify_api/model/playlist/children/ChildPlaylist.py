
from uuid import UUID
from django.db import models
from django.utils import timezone
from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel
from bodzify_api.model.user.User import User

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.ChildPlaylistManager import ChildPlaylistManager


class ChildPlaylist(BaseModel):
    # This fields must be overriden in each child class so that the related_name is unique.
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True)

    objects = ChildPlaylistManager()

    class Meta:
        abstract = True

    @property
    def uuid(self) -> UUID:
        return self.base_playlist.uuid

    @property
    def user(self) -> User:
        return self.base_playlist.user

    @property
    def created_on(self) -> timezone.datetime:
        return self.base_playlist.created_on

    @property
    def updated_on(self) -> timezone.datetime:
        return self.base_playlist.updated_on

    @property
    def library_tracks(self) -> models.QuerySet:
        return self.base_playlist.library_tracks  # type: ignore

    @property
    def library_tracks_count(self) -> int:
        return self.base_playlist.library_tracks_count

    @property
    def library_tracks_archived_count(self) -> int:
        return self.base_playlist.library_tracks_archived_count

    @property
    def duration_in_sec(self) -> int:
        return self.base_playlist.duration_in_sec

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        return self.base_playlist.duration_str_in_hour_min_sec

    @property
    def play_count(self) -> int:
        return self.base_playlist.play_count

    @play_count.setter
    def play_count(self, play_count: int):
        self.base_playlist.play_count = play_count

    @property
    def last_track_list_update_date(self) -> timezone.datetime:
        return self.base_playlist.last_track_list_update_date
