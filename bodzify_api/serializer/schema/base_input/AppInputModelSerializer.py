from typing import Counter, Dict, Any
from rest_framework import serializers
from bodzify_api.utils.validation_error_utils import raise_unknown_fields_error, raise_duplicate_fields_error


class AppInputModelSerializer(serializers.ModelSerializer):
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise_unknown_fields_error(list(unknown_keys))

        field_names = list(data.keys())
        field_counts = Counter(field_names)
        duplicates = [field for field, count in field_counts.items() if count > 1]
        if duplicates:
            raise_duplicate_fields_error(duplicates)

        return data
