from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.base_input.BaseInputModelSerializer import BaseInputModelSerializer
from .Fields import Fields


class CriteriaPostSerializer(BaseInputModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
