#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class LibTrackWithoutAlbumAndPlaylistSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [
            LIB_TRACK_ATTRIBUTES_LABEL.UUID,
            LIB_TRACK_ATTRIBUTES_LABEL.RELATIVE_URL,
            LIB_TRACK_ATTRIBUTES_LABEL.FILENAME,
            LIB_TRACK_ATTRIBUTES_LABEL.FILE_EXTENSION,
            LIB_TRACK_ATTRIBUTES_LABEL.FILE_EXISTS,
            LIB_TRACK_ATTRIBUTES_LABEL.TITLE,
            LIB_TRACK_ATTRIBUTES_LABEL.ARTIST,
            LIB_TRACK_ATTRIBUTES_LABEL.GENRE,
            LIB_TRACK_ATTRIBUTES_LABEL.DURATION,
            LIB_TRACK_ATTRIBUTES_LABEL.RATING,
            LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE,
            LIB_TRACK_ATTRIBUTES_LABEL.ADDED_ON]
