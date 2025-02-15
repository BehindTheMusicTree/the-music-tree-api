from rest_framework.fields import CharField

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from .Fields import Fields


class CriteriaPostSerializer(AppModelSerializer):
    name = CharField(max_length=settings.CRITERIA_NAME_LEN_MAX, allow_blank=False)

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
