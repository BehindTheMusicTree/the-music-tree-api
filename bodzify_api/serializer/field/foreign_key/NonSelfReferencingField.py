from typing import TypeVar, Generic, Any, Optional
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

T = TypeVar('T', bound=models.Model)


class NonSelfReferencingField(PrivateUuidField[T], Generic[T]):
    default_error_messages = {
        'self_reference': _('The object cannot reference itself.')
    }

    def to_internal_value(self, data: Any) -> Optional[T]:
        uuid = super().to_internal_value(data)
        instance = self.parent.instance

        if instance and uuid and instance.uuid == uuid:
            raise AppValidationError(
                field=str(self.field_name),
                message=self.error_messages['self_reference'],
                code=FieldValidationErrorCode.SELF_REFERENCE
            )

        if uuid:
            queryset = self.get_queryset()
            if queryset is None:
                raise ImproperlyConfigured("Queryset must be set for this field")
            return queryset.get(uuid=uuid)
        return None
