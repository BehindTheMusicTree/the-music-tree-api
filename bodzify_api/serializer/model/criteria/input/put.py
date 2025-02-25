from rest_framework.fields import CharField

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.foreign_key.DescendantAwareField import     DescendantAwareField
from bodzify_api.serializer.PutSerializer import PutSerializer

from .Fields import Fields


class CriteriaPutSerializer(PutSerializer):
    name = CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, required=False)
    parent: DescendantAwareField = DescendantAwareField(queryset=Criteria.objects.all(),  # type: ignore
                                                        required=False,
                                                        allow_null=True)

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
