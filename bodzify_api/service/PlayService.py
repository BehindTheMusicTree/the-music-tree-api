
from multiprocessing import context
from bodzify_api.model.user.User import User
from django.contrib.contenttypes.models import ContentType
from requests import Request

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.play.input.model import Fields as SaveFields
from bodzify_api.serializer.schema.play.input.model import PlayModelSerializer
from bodzify_api.serializer.schema.play.input.schema.endpoint.post import Fields as PostFields
from bodzify_api.serializer.schema.play.input.schema.endpoint.post import PlayPostSerializer
from bodzify_api.serializer.schema.play.input.schema.schema import PlaySchemaSerializer
from bodzify_api.service.Service import Service


class PlayService(Service):

    def _get_schema_serializer(self, oldinstance, schema_data: dict, request: Request):
        return PlaySchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request):
        return PlayModelSerializer(data=model_data, partial=partial, context={'request': request})

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_model_data_from_schema_data_not_including_user_field(self,
                                                                  user: User,
                                                                  schema_data: dict,
                                                                  oldinstance=None) -> dict:
        model_data = dict()

        content_object_uuid = schema_data.get(PostFields.CONTENT_OBJECT_UUID)

        content_object = BasePlaylist.objects.filter(user=user, uuid=content_object_uuid).first()
        if not content_object:
            content_object = LibraryTrack.objects.get(user=user, uuid=content_object_uuid)
        content_object.play_count += 1
        content_object.save()

        model_data[SaveFields.OBJECT_UUID] = content_object.uuid

        content_type = ContentType.objects.get_for_model(content_object)
        model_data[SaveFields.CONTENT_TYPE] = content_type.pk

        return model_data
