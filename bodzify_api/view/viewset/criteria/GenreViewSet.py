#!/usr/bin/env python

from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds


class GenreViewSet(CriteriaViewSet):
  def __init__(self, **kwargs): 
    super(GenreViewSet,self).__init__(
      criteriaTypeId=CriteriaTypesIds.GENRE, 
      playlistTypeId=PlaylistTypeIds.GENRE,
      **kwargs)