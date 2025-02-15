from django.db import models
from rest_framework.serializers import ModelSerializer

from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.field.PrivateUuidField import PrivateUuidField
from bodzify_api.serializer.field.NonSelfReferencingField import NonSelfReferencingField


class AppModelSerializer(AppValidationSerializer, ModelSerializer):
    """
    Base model serializer that provides consistent field mapping and validation.

    This serializer:
    1. Uses PrivateUuidField for foreign key fields automatically
    2. Uses NonSelfReferencingField for self-referential foreign keys
    3. Validates both existence and ownership of foreign key values
    4. Prevents self-referential relationships where appropriate
    5. Inherits common validation from AppValidationSerializer
    6. Maintains ModelSerializer's automatic field generation
    """

    def build_relational_field(self, field_name, relation_info):
        """
        Override to use appropriate field types for foreign keys.
        - NonSelfReferencingField for self-referential foreign keys
        - PrivateUuidField for other foreign keys
        """
        field_class, field_kwargs = super().build_relational_field(field_name, relation_info)
        if isinstance(relation_info.model_field, models.ForeignKey):
            # Check if the foreign key references the same model it's defined on
            if relation_info.model_field.remote_field.model == relation_info.model_field.model:
                field_class = NonSelfReferencingField
            else:
                field_class = PrivateUuidField
            field_kwargs['queryset'] = relation_info.model_field.remote_field.model.objects.all()
        return field_class, field_kwargs
