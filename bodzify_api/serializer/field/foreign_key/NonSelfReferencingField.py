from typing import Any, Generic, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.uuid.UuidModel import UuidModel
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField

T = TypeVar('T', bound=models.Model)


class NonSelfReferencingField(PrivateUuidField[T], Generic[T]):
    default_error_messages = {
        'self_reference': _('The object cannot reference itself.')
    }

    def to_internal_value(self, data: Any) -> T | None:
        object: UuidModel | None = PrivateUuidField.to_internal_value(self, data)
        if not object:
            return None

        instance = self.parent.instance

        if instance and object.uuid and instance.uuid == object.uuid:
            raise AppValidationException(
                field_name=str(self.field_name),
                message=self.error_messages['self_reference'],
                field_validation_error_code=FieldValidationErrorCode.SELF_REFERENCE
            )

        if object.uuid:
            queryset = self.get_queryset()
            if queryset is None:
                raise ImproperlyConfigured("Queryset must be set for this field")
            return queryset.get(uuid=object.uuid)
        return None
