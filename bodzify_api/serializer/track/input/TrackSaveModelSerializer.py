#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class TrackSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [LIB_TRACK_ATTRIBUTES_LABEL.USER,
                  LIB_TRACK_ATTRIBUTES_LABEL.FILE,
                  LIB_TRACK_ATTRIBUTES_LABEL.TITLE,
                  LIB_TRACK_ATTRIBUTES_LABEL.ARTIST,
                  LIB_TRACK_ATTRIBUTES_LABEL.ALBUM,
                  LIB_TRACK_ATTRIBUTES_LABEL.GENRE,
                  LIB_TRACK_ATTRIBUTES_LABEL.DURATION,
                  LIB_TRACK_ATTRIBUTES_LABEL.RATING,
                  LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE]
