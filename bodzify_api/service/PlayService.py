#!/usr/bin/env python

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.play.input.schema.endpoint.PlayPostSchemaSerializer import PlayPostSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.play.input.schema.PlaySaveSchemaSerializer import PlaySaveSchemaSerializer
from bodzify_api.serializer.play.input.PlaySaveModelSerializer import PlaySaveModelSerializer, FIELDS as SAVE_FIELDS
from bodzify_api.service.Service import Service


class PlayService(Service):

    def _get_post_serializer(self, post_data: dict):
        return PlayPostSerializer(data=post_data)

    def _get_save_schema_serializer(self, old_instance, save_schema_data: dict, request):
        return PlaySaveSchemaSerializer(data=save_schema_data, context={'request': request})

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return PlaySaveModelSerializer(data=save_model_data)

    def _get_save_schema_data_from_post_data(self, post_data: dict) -> dict:
        return post_data

    def _get_save_model_data_from_save_schema_data_not_including_user_field(self,
                                                                            user: User,
                                                                            save_schema_data: dict,
                                                                            old_instance=None) -> dict:
        save_model_data = dict()

        content_object_uuid = save_schema_data.get(POST_FIELDS.CONTENT_OBJECT_UUID)

        content_object = Playlist.objects.filter(user=user, uuid=content_object_uuid).first()
        if not content_object:
            content_object = LibraryTrack.objects.get(user=user, uuid=content_object_uuid)

        save_model_data[SAVE_FIELDS.OBJECT_UUID] = content_object.uuid

        content_type = ContentType.objects.get_for_model(content_object)
        save_model_data[SAVE_FIELDS.CONTENT_TYPE] = content_type.pk

        return save_model_data
