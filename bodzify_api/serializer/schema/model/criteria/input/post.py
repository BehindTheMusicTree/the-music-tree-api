
from rest_framework.serializers import ModelSerializer

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.field.UniquePerUserNameField import UniquePerUserNameField
from bodzify_api.serializer.field.foreign_key.DescendantAwareField import DescendantAwareField
from .Fields import Fields


class CriteriaPostSerializer(ModelSerializer, AppValidationSerializer):
    name = UniquePerUserNameField(max_length=settings.CRITERIA_NAME_LEN_MAX, allow_blank=False, model=Criteria)
    parent = DescendantAwareField(  # type: ignore
        queryset=Criteria.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
