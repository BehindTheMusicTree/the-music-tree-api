#!/usr/bin/env python

from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesLabels

class GenreViewSet(CriteriaViewSet):
  def __init__(self, criteriaTypeLabel=CriteriaTypesLabels.GENRE, **kwargs): 
    super(GenreViewSet,self).__init__(criteriaTypeLabel, **kwargs)