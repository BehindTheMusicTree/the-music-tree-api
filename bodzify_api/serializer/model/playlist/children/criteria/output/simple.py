
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.model.playlist.children.criteria.output.Fields import Fields as AvailableFields
from bodzify_api.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    CRITERIA = AvailableFields.CRITERIA
    PARENT = AvailableFields.PARENT
    ROOT = AvailableFields.ROOT
    CREATED_ON = AvailableFields.CREATED_ON
    UPDATED_ON = AvailableFields.UPDATED_ON


class CriteriaPlaylistSimpleSerializer(serializers.ModelSerializer):
    criteria = CriteriaSimpleSerializer()
    parent = CriteriaPlaylistMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)

    def to_representation(self, instance):
        if not isinstance(instance, CriteriaPlaylist):
            raise ImproperlyConfigured("Invalid instance type")
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
