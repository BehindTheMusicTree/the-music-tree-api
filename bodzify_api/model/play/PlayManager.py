from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields
from bodzify_api.serializer.schema.model.play.input.schema.endpoint.Fields import Fields as PostFields
from .Fields import Fields


class PlayManager(StandardResourceManager):

    def create(self, **kwargs):
        content_object_uuid = kwargs.pop(PostFields.CONTENT_OBJECT_UUID)
        content_object = None
        try:
            content_object = LibraryTrack.objects.get(uuid=content_object_uuid)
            content_type = ContentType.objects.get_for_model(LibraryTrack)
        except ObjectDoesNotExist:
            content_object = Playlist.objects.get(uuid=content_object_uuid)
            content_type = ContentType.objects.get_for_model(Playlist)

        if not isinstance(content_object, TrackablePlayCount):
            raise ImproperlyConfigured(f"Object {content_object} does not support play count")

        content_object.play_count += 1
        content_object.save(update_fields=[TrackablePlayCountFields.PLAY_COUNT])

        kwargs[Fields.CONTENT_TYPE] = content_type
        kwargs[Fields.OBJECT_PK] = content_object_uuid
        play = super().create(**kwargs)

        return play
