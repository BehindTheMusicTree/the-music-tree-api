
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import \
    PrivateUuidField


class CriteriaField(PrivateUuidField):

    def __init__(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = Criteria.objects.all()
        super().__init__(queryset=queryset, **kwargs)
