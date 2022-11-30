def getCommonCriteria(criteriaA, criteriaB):
    criteriaATreeItem = criteriaA
    while True:
        criteriaBTreeItem = criteriaB
        while criteriaBTreeItem is not None:
            if criteriaATreeItem == criteriaBTreeItem:
                return criteriaBTreeItem
            else:
                criteriaBTreeItem = criteriaBTreeItem.parent
        criteriaATreeItem = criteriaATreeItem.parent  