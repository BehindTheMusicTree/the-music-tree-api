from typing import Union

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.play.PlayManager import PlayManager
from bodzify_api.model.private_unique_resource.PrivateUniqueResource import PrivateUniqueResource
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from .Fields import Fields


class Play(PrivateUniqueResource):
    content_type = AppForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.UUIDField()
    content_object: Union[LibraryTrack, Playlist] = GenericForeignKey(
        Fields.CONTENT_TYPE, Fields.OBJECT_PK)  # type: ignore

    objects: PlayManager = PlayManager()

    def __str__(self) -> str:
        return f"{self.uuid} | {self.content_type} | {self.object_pk} | {self.content_object} | {self.created_on}"

    class Meta:
        verbose_name = 'Play'
        verbose_name_plural = 'Plays'
        indexes = [models.Index(fields=[Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_PK]),]
