#!/usr/bin/env python

from typing import Any, Dict, List
from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from bodzify_api.model.track.LibraryTrack import AttributesLabel as LibTrackAttributesLabels
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.detailed \
    import CriteriaTypeSerializer, Fields as CriteriaTypeFields
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant \
    import CriteriaAscendantRelationWithoutAscendantSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_descendant \
    import CriteriaAscendantRelationWithoutDescendantSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root \
    import CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer

from bodzify_api.serializer.track.output.without_playlists_and_album_and_genre \
    import LibTrackWithoutAlbumPlaylistGenreSerializer


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    DESCENDANTS = AttributesLabel.DESCENDANTS


class CriteriaWithDescendantsSerializer(serializers.ModelSerializer):
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabel.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.DESCENDANTS]
