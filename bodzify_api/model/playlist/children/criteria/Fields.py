from django.db import models
from typing import Dict, Any, TYPE_CHECKING

from bodzify_api.model.criteria.Criteria import Criteria, Fields as ModelFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, Fields as BasePlaylistFields
from bodzify_api.model.playlist.children.ChildPlaylist import ChildPlaylist
from bodzify_api.model.playlist.children.Fields import Fields as ChildFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager
from bodzify_api.utils.model import SaveContext


class Fields:
    BASE_PLAYLIST = ChildFields.BASE_PLAYLIST
    UUID = ChildFields.UUID
    USER = ChildFields.USER
    CREATED_ON = ChildFields.CREATED_ON
    UPDATED_ON = ChildFields.UPDATED_ON
    LIB_TRACKS = ChildFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = ChildFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildFields.LAST_TRACK_LIST_UPDATE_DATE
    CRITERIA = 'criteria'
    PARENT = 'parent'
    ROOT = 'root'
    NAME = 'name'
