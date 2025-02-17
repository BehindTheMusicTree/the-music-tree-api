from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from bodzify_api.serializer.field.foreign_key.NonSelfReferencingField import NonSelfReferencingField


class DescendantAwareField(NonSelfReferencingField):

    default_error_messages = {
        'descendant_reference': _('Cannot reference a descendant of the object.')
    }

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        instance = self.parent.instance

        if instance:
            if not hasattr(instance, 'is_descendant_of'):
                raise ImproperlyConfigured("Instance must have is_descendant_of method.")

            if value and value.is_descendant_of(instance):
                self.fail('descendant_reference')

        return value
