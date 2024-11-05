from ...Criteria import Fields as CriteriaFields


class Fields:
    MODEL = 'Genre'
    CREATED_ON = CriteriaFields.CREATED_ON
    UPDATED_ON = CriteriaFields.UPDATED_ON
    USER = CriteriaFields.USER
    UUID = CriteriaFields.UUID
    LIB_TRACKS = CriteriaFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = CriteriaFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = CriteriaFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = CriteriaFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = CriteriaFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = CriteriaFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = CriteriaFields.NAME
    PARENT = CriteriaFields.PARENT
    CHILD = CriteriaFields.CHILD
    ASCENDANT = CriteriaFields.ASCENDANT
    ASCENDANTS = CriteriaFields.ASCENDANTS
    DESCENDANT = CriteriaFields.DESCENDANT
    DESCENDANTS = CriteriaFields.DESCENDANTS
    CRITERIA_ASCENDANT_RELATION_ASCENDANTS = 'genre_ascendant_rel_ascendants'
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = 'genre_ascendant_rel_descendants'
    CHILDREN = CriteriaFields.CHILDREN
    ROOT = CriteriaFields.ROOT
    CRITERIA_PLAYLIST = CriteriaFields.CRITERIA_PLAYLIST
