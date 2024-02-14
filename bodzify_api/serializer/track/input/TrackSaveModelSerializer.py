#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class TrackSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [ATTRIBUTES_LABEL.USER,
                  ATTRIBUTES_LABEL.FILE,
                  ATTRIBUTES_LABEL.TITLE,
                  ATTRIBUTES_LABEL.ARTIST,
                  ATTRIBUTES_LABEL.ALBUM,
                  ATTRIBUTES_LABEL.GENRE,
                  ATTRIBUTES_LABEL.DURATION,
                  ATTRIBUTES_LABEL.RATING,
                  ATTRIBUTES_LABEL.LANGUAGE]
