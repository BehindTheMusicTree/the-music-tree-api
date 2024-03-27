#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE = ATTRIBUTES_LABEL.FILE
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE


class TrackSaveModelSerializer(InputEndpointSerializer):

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.USER,
                  FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE]
