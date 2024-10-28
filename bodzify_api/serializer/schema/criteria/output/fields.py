#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Fields as ModelFields
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.serializer.schema.criteria.type.detailed import Fields as CriteriaTypeFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    UUID = ModelFields.UUID
    NAME = ModelFields.NAME
    LIB_TRACKS = ModelFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ModelFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ModelFields.LIB_TRACKS_ARCHIVED_COUNT
    LIB_TRACKS_TITLE = LibTrackFields.TITLE
    TYPE = ModelFields.TYPE
    TYPE_LABEL = CriteriaTypeFields.LABEL
    ROOT = ModelFields.ROOT
    PARENT = ModelFields.PARENT
    ASCENDANTS = ModelFields.ASCENDANTS
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = ModelFields.CRITERIA_ASCENDANT_RELATION_DESCENDANTS
    DESCENDANTS = ModelFields.DESCENDANTS
    CHILDREN = ModelFields.CHILDREN
    CRITERIA_PLAYLIST = ModelFields.CRITERIA_PLAYLIST
