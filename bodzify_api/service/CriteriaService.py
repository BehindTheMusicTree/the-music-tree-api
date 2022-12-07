#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames

def GetCommonCriteria(criteriaA, criteriaB):
    criteriaATreeItem = criteriaA
    while True:
        criteriaBTreeItem = criteriaB
        while criteriaBTreeItem is not None:
            if criteriaATreeItem == criteriaBTreeItem:
                return criteriaBTreeItem
            else:
                criteriaBTreeItem = criteriaBTreeItem.parent
        criteriaATreeItem = criteriaATreeItem.parent
