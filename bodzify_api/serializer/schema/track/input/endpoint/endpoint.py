#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.UserFilteredUUIDField import UserFilteredUUIDField
from bodzify_api.serializer.schema.endpoint import InputEndpointSerializer
from bodzify_api.serializer.schema.track.input.schema import Fields as SaveSchemaFields

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""
position_in_album_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album position is."""


class Fields:
    FILE = SaveSchemaFields.FILE
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = SaveSchemaFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = SaveSchemaFields.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES = SaveSchemaFields.ARTISTS_NAMES
    ALBUM_NAME = SaveSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = SaveSchemaFields.ALBUM_ARTISTS_NAMES
    POSITION_IN_ALBUM = SaveSchemaFields.POSITION_IN_ALBUM
    GENRE_UUID = SaveSchemaFields.GENRE_UUID
    GENRE_NAME = SaveSchemaFields.GENRE_NAME
    RATING = SaveSchemaFields.RATING
    LANGUAGE = SaveSchemaFields.LANGUAGE
    ARCHIVED = SaveSchemaFields.ARCHIVED


class LibTrackEndPointSerializer(InputEndpointSerializer):
    track_file_fingerprint_must_be_unique = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX,
                                  required=False,
                                  allow_blank=True,
                                  allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)
    artists_names = serializers.CharField(max_length=settings.ARTISTS_NAMES_LEN_MAX,
                                          required=False,
                                          allow_blank=True,
                                          allow_null=True)
    album_name = serializers.CharField(max_length=settings.ALBUM_NAME_LEN_MAX,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
    album_artists_names = serializers.CharField(max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
                                                required=False,
                                                allow_blank=True,
                                                allow_null=True)
    position_in_album = serializers.IntegerField(required=False, allow_null=True)
    genre_uuid = UserFilteredUUIDField(queryset=Criteria.objects,
                                       required=False,
                                       allow_null=False)
    genre_name = serializers.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
    rating = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    language = serializers.CharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX,
                                     required=False,
                                     allow_blank=True,
                                     allow_null=True)
    archived = serializers.BooleanField(required=False)

    def validate(self, data):
        if Fields.GENRE_UUID in data and Fields.GENRE_NAME in data:
            if data[Fields.GENRE_UUID] not in ['', None] and data[Fields.GENRE_NAME] not in ['', None]:
                raise serializers.ValidationError(
                    {Fields.GENRE_NAME: "Genre name and genre uuid cannot be specified at the same time."}
                )

        if Fields.ALBUM_ARTISTS_NAMES in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise serializers.ValidationError({Fields.ALBUM_ARTISTS_NAMES: error_message})

        if Fields.POSITION_IN_ALBUM in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = position_in_album_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = position_in_album_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise serializers.ValidationError({Fields.ALBUM_NAME: error_message})

        if Fields.RATING in data:
            value = data[Fields.RATING]
            if value and value != '':
                try:
                    value = int(value)
                except ValueError:
                    raise serializers.ValidationError({Fields.RATING: "Rating must be an integer."})

        return super().validate(data)
