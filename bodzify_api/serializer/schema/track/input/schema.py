
from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.serializer.field.UserFilteredUUIDField import UserFilteredUUIDField
from bodzify_api.serializer.schema.track.input.model import Fields as SaveModelFields


class Fields:
    USER = SaveModelFields.USER
    FILE = SaveModelFields.FILE
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = SaveModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = SaveModelFields.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES = f"{SaveModelFields.ARTISTS}_{ArtistFields.NAME}s"
    ALBUM_NAME = f"{SaveModelFields.ALBUM}_name"
    ALBUM_ARTISTS_NAMES = f"{SaveModelFields.ALBUM}_artists_names"
    POSITION_IN_ALBUM = SaveModelFields.POSITION_IN_ALBUM
    GENRE_UUID = f"{SaveModelFields.GENRE}_uuid"
    GENRE_NAME = f"{SaveModelFields.GENRE}_name"
    RATING = SaveModelFields.RATING
    LANGUAGE = SaveModelFields.LANGUAGE
    ARCHIVED = SaveModelFields.ARCHIVED


class LibTrackSchemaSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
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
    position_in_album = serializers.IntegerField(required=False, allow_null=True)
    album_artists_names = serializers.CharField(max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
                                                required=False,
                                                allow_blank=True,
                                                allow_null=True)
    genre_uuid = UserFilteredUUIDField(queryset=Criteria.objects,
                                       required=False,
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
                  Fields.ARTISTS_NAMES,
                  Fields.ALBUM_NAME,
                  Fields.ALBUM_ARTISTS_NAMES,
                  Fields.GENRE_UUID,
                  Fields.GENRE_NAME,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.ARCHIVED]
