from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME_PUBLIC = AvailableFields.NAME


class CriteriaMinimumSerializer(AppModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME_PUBLIC
        ]
