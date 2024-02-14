#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class TrackWithoutAlbumAndPlaylistSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [
            ATTRIBUTES_LABEL.UUID,
            ATTRIBUTES_LABEL.RELATIVE_URL,
            ATTRIBUTES_LABEL.FILENAME,
            ATTRIBUTES_LABEL.FILE_EXTENSION,
            ATTRIBUTES_LABEL.FILE_EXISTS,
            ATTRIBUTES_LABEL.TITLE,
            ATTRIBUTES_LABEL.ARTIST,
            ATTRIBUTES_LABEL.GENRE,
            ATTRIBUTES_LABEL.DURATION,
            ATTRIBUTES_LABEL.RATING,
            ATTRIBUTES_LABEL.LANGUAGE,
            ATTRIBUTES_LABEL.ADDED_ON]
