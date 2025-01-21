
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.PrivateUuidField import PrivateUuidField


class CriteriaField(PrivateUuidField):

    def __init__(self, queryset, **kwargs):
        if not queryset:
            queryset = Criteria.objects.all()
        super().__init__(queryset, **kwargs)
