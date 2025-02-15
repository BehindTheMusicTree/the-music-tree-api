from django.utils.translation import gettext_lazy as _

from bodzify_api.serializer.field.PrivateUuidField import PrivateUuidField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class NonSelfReferencingField(PrivateUuidField):
    default_error_messages = {
        'self_reference': _('The object cannot reference itself.')
    }

    def to_internal_value(self, data):
        uuid = super().to_internal_value(data)
        instance = self.parent.instance

        if instance and uuid and instance.uuid == uuid:
            raise AppValidationError(
                field=str(self.field_name),
                message=self.error_messages['self_reference'],
                code=FieldValidationErrorCode.SELF_REFERENCE
            )

        if uuid:
            return self.queryset.get(uuid=uuid)
        return None
