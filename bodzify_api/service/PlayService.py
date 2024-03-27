#!/usr/bin/env python

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import QueryDict
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.play.input.schema.PlayPostSchemaSerializer import PlayPostSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.play.input.schema.PlaySaveSchemaSerializer import PlaySaveSchemaSerializer
from bodzify_api.serializer.play.input.PlaySaveModelSerializer import PlaySaveModelSerializer, FIELDS as SAVE_FIELDS
from bodzify_api.service.Service import Service


class PlayService(Service):

    def _get_post_schema_serializer(self, post_schema_data: QueryDict):
        return PlayPostSerializer(data=post_schema_data)

    def _get_put_schema_serializer(self, user: User, old_instance, put_schema_data: QueryDict):
        raise NotImplementedError("You should implement this method in a subclass")

    def _get_save_schema_serializer(self, old_instance, save_schema_data: QueryDict, request):
        return PlaySaveSchemaSerializer(data=save_schema_data, context={'request': request})

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool):
        return PlaySaveModelSerializer(data=save_model_data)

    def _get_save_model_data_from_save_schema_data_not_including_user_field(self,
                                                                            user,
                                                                            save_schema_data: QueryDict,
                                                                            old_instance=None) -> QueryDict:
        save_model_data = QueryDict(mutable=True)

        content_object_uuid = save_schema_data.get(POST_FIELDS.CONTENT_OBJECT_UUID)
        content_object = Playlist.objects.get(uuid=content_object_uuid)
        save_model_data[SAVE_FIELDS.OBJECT_ID] = content_object.uuid

        content_type = ContentType.objects.get_for_model(content_object)
        save_model_data[SAVE_FIELDS.CONTENT_TYPE] = content_type.pk

        return save_model_data
