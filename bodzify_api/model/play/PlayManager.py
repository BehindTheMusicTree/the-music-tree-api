from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from bodzify_api.serializer.schema.model.play.input.schema.endpoint.Fields import Fields as PostFields

from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from .Fields import Fields


class PlayManager(StandardResourceManager):

    def create(self, **kwargs):
        content_object_uuid = kwargs.pop(PostFields.CONTENT_OBJECT_UUID)
        try:
            LibraryTrack.objects.get(uuid=content_object_uuid)
            content_type = ContentType.objects.get_for_model(LibraryTrack)
        except ObjectDoesNotExist:
            Playlist.objects.get(uuid=content_object_uuid)
            content_type = ContentType.objects.get_for_model(Playlist)

        kwargs[Fields.CONTENT_TYPE] = content_type
        kwargs[Fields.OBJECT_PK] = content_object_uuid
        return super().create(**kwargs)
