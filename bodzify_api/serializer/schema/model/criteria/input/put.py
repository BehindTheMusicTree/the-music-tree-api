from rest_framework.fields import CharField

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.DescendantAwareField import DescendantAwareField
from bodzify_api.serializer.AppPutModelSerializer import AppPutModelSerializer
from .Fields import Fields


class CriteriaPutSerializer(AppPutModelSerializer):
    parent: DescendantAwareField = DescendantAwareField(queryset=Criteria.objects.all(),
                                                        required=False,
                                                        allow_null=True)
    name = CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, required=False)

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
