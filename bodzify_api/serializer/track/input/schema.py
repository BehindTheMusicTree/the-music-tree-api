#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.model import FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.album.input.model import FIELDS as ALBUM_SAVE_MODEL_FIELDS


class FIELDS:
    USER = SAVE_MODEL_FIELDS.USER
    FILE = "file"
    SHOULD_CHECK_IF_FINGERPRINT_EXISTS = "should_check_if_fingerprint_exists"
    DURATION_IN_SEC = SAVE_MODEL_FIELDS.DURATION_IN_SEC
    TITLE = SAVE_MODEL_FIELDS.TITLE
    ARTIST_NAME = SAVE_MODEL_FIELDS.ARTIST + "_name"
    ALBUM_NAME = SAVE_MODEL_FIELDS.ALBUM + "_name"
    ALBUM_ARTISTS_NAMES_STR = ALBUM_SAVE_MODEL_FIELDS.ALBUM_ARTISTS + "_names_string"
    GENRE_UUID = SAVE_MODEL_FIELDS.GENRE + "_uuid"
    GENRE_NAME = SAVE_MODEL_FIELDS.GENRE + "_name"
    RATING = SAVE_MODEL_FIELDS.RATING
    LANGUAGE = SAVE_MODEL_FIELDS.LANGUAGE
    FORCE_TITLE_GENERATION = "force_title_generation"


class LibTrackSchemaSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    should_check_if_fingerprint_exists = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX,
                                  required=False,
                                  allow_blank=True,
                                  allow_null=True)
    artist_name = serializers.CharField(max_length=settings.ARTIST_NAME_LEN_MAX,
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
    genre_uuid = serializers.CharField(max_length=settings.CRITERIA_NAME_LEN_MAX,
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
    force_title_generation = serializers.BooleanField(required=False)

    class Meta:
        fields = [FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST_NAME,
                  FIELDS.ALBUM_NAME,
                  FIELDS.ALBUM_ARTISTS_NAMES_STR,
                  FIELDS.GENRE_UUID,
                  FIELDS.GENRE_NAME,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.FORCE_TITLE_GENERATION,]

    def validate(self, attrs):
        if FIELDS.GENRE_UUID in attrs and attrs[FIELDS.GENRE_UUID] not in ['', None] and not Criteria.objects.filter(
                uuid=attrs[FIELDS.GENRE_UUID],
                user=self.context['request'].user).exists():
            raise serializers.ValidationError({FIELDS.GENRE_UUID: "The genre UUID does not exist."})

        return super().validate(attrs)
