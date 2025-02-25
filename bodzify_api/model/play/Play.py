from django.contrib.contenttypes.models import ContentType
from django.db import models

from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.field.foreign_key.PrivateUuidGenericForeignKey import \
    PrivateUuidGenericForeignKey
from bodzify_api.model.play.PlayManager import PlayManager
from bodzify_api.model.private_unique_resource.PrivateUniqueResource import \
    PrivateUniqueResource
from bodzify_api.model.trackable_play_count.TrackablePlayCount import \
    TrackablePlayCount

from .Fields import Fields


class Play(PrivateUniqueResource):
    """Tracks plays of any model that inherits from TrackablePlayCount.

    Uses Django's generic foreign key mechanism to reference the played content,
    which can be either a LibraryTrack or a Playlist.
    """
    content_type = AppForeignKey(ContentType, on_delete=models.CASCADE)
    content_uuid = models.UUIDField(db_column='object_pk')
    content: TrackablePlayCount = PrivateUuidGenericForeignKey(  # type: ignore
        ct_field=Fields.CONTENT_TYPE, fk_field=Fields.CONTENT_UUID)

    objects: PlayManager = PlayManager()

    def __str__(self) -> str:
        return f"{
            self.uuid}  | {
            self.content_type}  | {
            self.content_uuid}  | {
            self.content}  | {
            self.created_on} "

    class Meta:
        verbose_name = 'Play'
        verbose_name_plural = 'Plays'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.CONTENT_TYPE, Fields.CONTENT_UUID]),
        ]
