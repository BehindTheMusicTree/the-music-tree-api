from uuid import UUID
from typing import Optional, List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models.query import QuerySet

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria


class CriteriaField(serializers.RelatedField):
    """
    A unified field that handles both UUID and name-based criteria inputs.
    Automatically detects input type and processes accordingly.
    Can be used directly or inherited by specific criteria type fields.
    """
    queryset: QuerySet
    char_field: Optional[serializers.CharField]

    def __init__(self, queryset: QuerySet = Criteria.objects.all(), input_types: Optional[List[str]] = None, **kwargs):
        self.input_types = input_types or ['uuid', 'name']
        if not all(t in ['uuid', 'name'] for t in self.input_types):
            raise ValueError("input_types must only contain 'uuid' and/or 'name'")

        self.queryset = queryset
        self._allow_blank = kwargs.get('allow_blank', True)
        self._allow_null = kwargs.get('allow_null', True)

        # Create CharField for name validation if name input is enabled
        self.char_field = None
        if 'name' in self.input_types:
            char_kwargs = {
                'max_length': settings.CRITERIA_NAME_LEN_MAX,
                'allow_blank': self._allow_blank,
                'allow_null': self._allow_null
            }
            self.char_field = serializers.CharField(**char_kwargs)

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data in [None, '']:
            if not self._allow_null:
                raise ValidationError("This field may not be null.")
            return None

        # Try UUID first if enabled
        if 'uuid' in self.input_types:
            try:
                # Check if it's a valid UUID
                uuid_val = UUID(str(data))
                return self.queryset.get(uuid=uuid_val)
            except (ValueError, TypeError):
                # Not a UUID, continue to name handling
                pass
            except self.queryset.model.DoesNotExist:
                raise ValidationError(f"Criteria with UUID {data} does not exist.")

        # Try name if enabled
        if 'name' in self.input_types and self.char_field:
            try:
                # Validate using CharField first
                validated_name = self.char_field.to_internal_value(data)
                
                request = self.context.get('request')
                if not request or not request.user:
                    raise ValidationError("Cannot process criteria name without valid request context.")
                
                return self.queryset.model.objects.get_or_create(user=request.user, name=validated_name)[0]
            except ValidationError as e:
                raise ValidationError(f"Invalid criteria name: {str(e)}")
            except Exception as e:
                raise ValidationError(f"Error processing criteria name: {str(e)}")

        raise ValidationError("Invalid input format for criteria field.")

    def to_representation(self, value):
        return str(value.uuid)