
from django.contrib.contenttypes.fields import GenericForeignKey

from api.serializer.field.foreign_key.UserContentObjectUuidField import PrivateContentUuidField


class PrivateUuidGenericForeignKey(GenericForeignKey):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_field_class = PrivateContentUuidField
