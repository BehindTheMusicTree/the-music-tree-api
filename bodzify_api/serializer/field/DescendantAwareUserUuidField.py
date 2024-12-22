from django.utils.translation import gettext_lazy as _

from bodzify_api.serializer.field.NonSelfReferencingUserUuidField import NonSelfReferencingUserUuidField


class DescendantAwareUserUuidField(NonSelfReferencingUserUuidField):
    """
    A custom field that always checks for descendant relationships.
    This is a specialized version of NonSelfReferencingUserUuidField that enforces
    descendant checking by default.
    """
    default_error_messages = {
        'descendant_reference': _('Cannot reference a descendant of the object.')
    }

    def to_internal_value(self, data):
        uuid = super().to_internal_value(data)
        instance = self.parent.instance

        if instance:
            if hasattr(instance, 'is_descendant_of'):
                obj = self.queryset.get(uuid=uuid)
                if obj.is_descendant_of(instance):
                    self.fail('descendant_reference')
            else:
                raise ValueError("Instance must have is_descendant_of method.")
