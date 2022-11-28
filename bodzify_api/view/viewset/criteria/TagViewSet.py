#!/usr/bin/env python

from bodzify_api.view.viewset.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesLabels

class TagViewSet(CriteriaViewSet):
  def __init__(self, criteriaTypeLabel=CriteriaTypesLabels.TAG, **kwargs): 
    super(TagViewSet,self).__init__(criteriaTypeLabel, **kwargs)