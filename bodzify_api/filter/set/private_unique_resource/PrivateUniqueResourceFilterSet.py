from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields


class PrivateUniqueResourceFilterSet(AppFilterSet):

    class Meta:
        model = Criteria
        fields = [Fields.CREATED_ON, Fields.UPDATED_ON]
