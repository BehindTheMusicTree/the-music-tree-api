#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.track.input.schema import Fields as SaveSchemaFields

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album artists name is."""
position_in_album_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be specified if album position is."""


class Fields:
    TRACK_FILE = SaveSchemaFields.FILE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
    TITLE = SaveSchemaFields.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES_STR = SaveSchemaFields.ARTISTS_NAMES_STR
    ALBUM_NAME = SaveSchemaFields.ALBUM_NAME
    ALBUM_ARTISTS_NAMES_STR = SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR
    POSITION_IN_ALBUM = SaveSchemaFields.POSITION_IN_ALBUM
    GENRE_UUID = SaveSchemaFields.GENRE_UUID
    GENRE_NAME = SaveSchemaFields.GENRE_NAME
    RATING = SaveSchemaFields.RATING
    LANGUAGE = SaveSchemaFields.LANGUAGE
    ARCHIVED = SaveSchemaFields.ARCHIVED


class LibTrackEndPointSerializer(InputEndpointSerializer):
    should_cancel_if_duplicate_fingerprint = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX,
                                  required=False,
                                  allow_blank=True,
                                  allow_null=True)
    force_title_generation = serializers.BooleanField(required=False)
    artists_names_str = serializers.CharField(max_length=settings.ARTISTS_NAMES_LEN_MAX,
                                              required=False,
                                              allow_blank=True,
                                              allow_null=True)
    album_name = serializers.CharField(max_length=settings.ALBUM_NAME_LEN_MAX,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
    album_artists_names_string = serializers.CharField(max_length=settings.ALBUM_ARTISTS_FIELD_LEN_MAX,
                                                       required=False,
                                                       allow_blank=True,
                                                       allow_null=True)
    position_in_album = serializers.IntegerField(required=False, allow_null=True)
    genre_uuid = serializers.CharField(max_length=settings.UUID_LEN,
                                       required=False,
                                       allow_blank=True,
                                       allow_null=True)
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
                    {Fields.GENRE_NAME: "Genre name and genre cannot be specified at the same time."}
                )

        if Fields.ALBUM_ARTISTS_NAMES_STR in data:
            error_message = None
            if Fields.ALBUM_NAME not in data:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE
            elif data[Fields.ALBUM_NAME] in [None, ""]:
                error_message = ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE

            if error_message:
                raise serializers.ValidationError({Fields.ALBUM_ARTISTS_NAMES_STR: error_message})

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
            if value is not None and value != '':
                try:
                    value = int(value)
                except ValueError:
                    raise serializers.ValidationError({Fields.RATING: "Rating must be an integer."})

        return super().validate(data)
