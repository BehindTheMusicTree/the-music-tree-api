from rest_framework.exceptions import ValidationError

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.base_input.AppInputModelSerializer import AppInputModelSerializer
from .Fields import Fields


class CriteriaPutSerializer(AppInputModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]

    def validate(self, data: dict):
        instance: Criteria = self.instance  # type: ignore
        value = data.get(Fields.PARENT)

        if instance and value:
            error_message = None
            if instance == value:
                error_message = "Cannot set the new parent as the criteria itself."
            elif value.is_descendant_of(instance):
                error_message = "Cannot set the new parent as one of the criteria's descendants."

            if error_message:
                raise ValidationError({Fields.PARENT: error_message})

        return super().validate(data)
