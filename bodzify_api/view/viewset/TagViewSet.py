#!/usr/bin/env python

from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds


class TagViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super(TagViewSet, self).__init__(
          criteriaTypeId=CriteriaTypesIds.TAG,
          playlistTypeId=PlaylistTypeIds.TAG,
          **kwargs)
