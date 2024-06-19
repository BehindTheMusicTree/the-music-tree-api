#!/usr/bin/env python

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.play.input.schema.endpoint.post import PlayPostSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.play.input.schema.schema import PlaySchemaSerializer
from bodzify_api.serializer.play.input.model import PlayModelSerializer, FIELDS as SAVE_FIELDS
from bodzify_api.service.Service import Service


class PlayService(Service):

    def _get_post_serializer(self, post_data: dict):
        return PlayPostSerializer(data=post_data)

    def _get_schema_serializer(self, old_instance, schema_data: dict, request):
        return PlaySchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, old_instance, model_data: dict, partial: bool):
        return PlayModelSerializer(data=model_data)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_model_data_from_schema_data_not_including_user_field(self,
                                                                  user: User,
                                                                  schema_data: dict,
                                                                  old_instance=None) -> dict:
        model_data = dict()

        content_object_uuid = schema_data.get(POST_FIELDS.CONTENT_OBJECT_UUID)

        content_object = BasePlaylist.objects.filter(user=user, uuid=content_object_uuid).first()
        if not content_object:
            content_object = LibraryTrack.objects.get(user=user, uuid=content_object_uuid)
        content_object.play_count += 1
        content_object.save()

        model_data[SAVE_FIELDS.OBJECT_UUID] = content_object.uuid

        content_type = ContentType.objects.get_for_model(content_object)
        model_data[SAVE_FIELDS.CONTENT_TYPE] = content_type.pk

        return model_data
