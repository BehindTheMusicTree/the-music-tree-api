from django.utils.translation import gettext_lazy as _

from bodzify_api.serializer.field.PrivateUuidField import PrivateUuidField


class NonSelfReferencingField(PrivateUuidField):
    """
    A custom field that prevents self-referential relationships in foreign keys.
    """
    default_error_messages = {
        'self_reference': _('The object cannot reference itself.')
    }

    def to_internal_value(self, data):
        uuid = super().to_internal_value(data)
        instance = self.parent.instance

        if instance and uuid and instance.uuid == uuid:
            self.fail('self_reference')

        if uuid:
            return self.queryset.get(uuid=uuid)
        return None
