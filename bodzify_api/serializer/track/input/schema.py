#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.Artist import AttributesLabels as ArtistAttributesLabels
from bodzify_api.serializer.track.input.model import Fields as SaveModelFields


class Fields:
    USER = SaveModelFields.USER
    FILE = "file"
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"
    DURATION_IN_SEC = SaveModelFields.DURATION_IN_SEC
    TITLE = SaveModelFields.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES_STR = f"{SaveModelFields.ARTISTS}_{ArtistAttributesLabels.NAME}s_str"
    ALBUM_NAME = f"{SaveModelFields.ALBUM}_name"
    ALBUM_ARTISTS_NAMES_STR = f"{SaveModelFields.ALBUM}_artists_names_str"
    POSITION_IN_ALBUM = SaveModelFields.POSITION_IN_ALBUM
    GENRE_UUID = f"{SaveModelFields.GENRE}_uuid"
    GENRE_NAME = f"{SaveModelFields.GENRE}_name"
    RATING = SaveModelFields.RATING
    LANGUAGE = SaveModelFields.LANGUAGE
    ARCHIVED = SaveModelFields.ARCHIVED


class LibTrackSchemaSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
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
    position_in_album = serializers.IntegerField(required=False, allow_null=True)
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

    class Meta:
        fields = [Fields.FILE,
                  Fields.TITLE,
                  Fields.FORCE_TITLE_GENERATION,
                  Fields.ARTISTS_NAMES_STR,
                  Fields.ALBUM_NAME,
                  Fields.ALBUM_ARTISTS_NAMES_STR,
                  Fields.GENRE_UUID,
                  Fields.GENRE_NAME,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.ARCHIVED]

    def validate(self, attrs):
        if Fields.GENRE_UUID in attrs and attrs[Fields.GENRE_UUID] not in ['', None] and not Criteria.objects.filter(
                uuid=attrs[Fields.GENRE_UUID],
                user=self.context['request'].user).exists():
            raise serializers.ValidationError({Fields.GENRE_UUID: "The genre UUID does not exist."})

        return super().validate(attrs)
