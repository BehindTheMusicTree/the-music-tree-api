#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin, AttributesLabels


class Fields:
    UUID = AttributesLabels.UUID
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class LibTrackMixinSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibTrackMixin
        fields = [Fields.UUID,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,]
