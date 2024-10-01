#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.model import Fields as SaveModelFields
from bodzify_api.model.Album import AttributesLabel as AttributesLabel


class Fields:
    USER = SaveModelFields.USER
    FILE = "file"
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"
    DURATION_IN_SEC = SaveModelFields.DURATION_IN_SEC
    TITLE = SaveModelFields.TITLE
    ARTIST_NAME = SaveModelFields.ARTIST + "_name"
    ALBUM_NAME = SaveModelFields.ALBUM + "_name"
    ALBUM_ARTISTS_NAMES_STR = AttributesLabel.ALBUM_ARTISTS + "_names_string"
    GENRE_UUID = SaveModelFields.GENRE + "_uuid"
    GENRE_NAME = SaveModelFields.GENRE + "_name"
    RATING = SaveModelFields.RATING
    LANGUAGE = SaveModelFields.LANGUAGE
    FORCE_TITLE_GENERATION = "force_title_generation"


class LibTrackSchemaSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    should_cancel_if_duplicate_fingerprint = serializers.BooleanField(required=False)
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
        fields = [Fields.FILE,
                  Fields.TITLE,
                  Fields.ARTIST_NAME,
                  Fields.ALBUM_NAME,
                  Fields.ALBUM_ARTISTS_NAMES_STR,
                  Fields.GENRE_UUID,
                  Fields.GENRE_NAME,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.FORCE_TITLE_GENERATION,]

    def validate(self, attrs):
        if Fields.GENRE_UUID in attrs and attrs[Fields.GENRE_UUID] not in ['', None] and not Criteria.objects.filter(
                uuid=attrs[Fields.GENRE_UUID],
                user=self.context['request'].user).exists():
            raise serializers.ValidationError({Fields.GENRE_UUID: "The genre UUID does not exist."})

        return super().validate(attrs)
