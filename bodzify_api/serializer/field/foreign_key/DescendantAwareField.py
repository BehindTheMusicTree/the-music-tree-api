from typing import TypeVar, Any, Optional, Protocol, runtime_checkable, Generic
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.relations import RelatedField
from rest_framework.serializers import BaseSerializer

from bodzify_api.serializer.field.foreign_key.NonSelfReferencingField import NonSelfReferencingField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


@runtime_checkable
class HasDescendantCheck(Protocol):
    def is_descendant_of(self, other: Any) -> bool:
        ...


T = TypeVar('T', bound=models.Model)


class DescendantAwareField(NonSelfReferencingField[T], Generic[T]):
    """
    A field that ensures the referenced object is not a descendant of the current object.
    Extends NonSelfReferencingField to prevent self-referencing and adds descendant checking.
    """

    default_error_messages = {
        'descendant_reference': _('Cannot reference a descendant of the object.')
    }

    def to_internal_value(self, data: Any) -> Optional[T]:
        # First validate through the parent class chain
        value = NonSelfReferencingField.to_internal_value(self, data)
        if value is None:
            return None

        instance = self.parent.instance
        if instance:
            if not hasattr(instance, 'is_descendant_of'):
                raise ImproperlyConfigured("Instance must have is_descendant_of method.")

            # We know value is of type T since it came from NonSelfReferencingField[T]
            model_instance = value
            if isinstance(model_instance, HasDescendantCheck) and model_instance.is_descendant_of(instance):
                raise AppValidationError(
                    field=str(self.field_name),
                    message=self.error_messages['descendant_reference'],
                    code=FieldValidationErrorCode.ANCESTOR_REFERENCE
                )

        return value
