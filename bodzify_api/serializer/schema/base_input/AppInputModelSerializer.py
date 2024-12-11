
from typing import Counter, Dict, Any, List
from rest_framework import serializers
import json
import re
from bodzify_api.utils.validation_error_utils import raise_unknown_fields_error, raise_duplicate_fields_error


class AppInputModelSerializer(serializers.ModelSerializer):
    def _get_raw_field_names(self, raw_data: str) -> List[str]:
        """Extract field names from raw JSON string."""
        # Remove whitespace and newlines between tokens to simplify parsing
        raw_data = re.sub(r'\s+', '', raw_data)

        # Find all field names using regex
        # This pattern matches field names in JSON, handling escaped quotes
        pattern = r'"((?:[^"\\]|\\.)*)":'
        matches = re.finditer(pattern, raw_data)

        # Return all field names found in the raw JSON
        return [match.group(1).replace('\\"', '"') for match in matches]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Check for unknown field
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise_unknown_fields_error(list(unknown_keys))

            # Check for duplicate fields in raw request data
            request = self.context.get('request')
            if request and hasattr(request, '_request'):
                try:
                    raw_data = request._request.body.decode('utf-8')
                    field_names = self._get_raw_field_names(raw_data)
                    field_counts = Counter(field_names)
                    duplicates = [field for field, count in field_counts.items() if count > 1]

                    if duplicates:
                        raise_duplicate_fields_error(duplicates)
                except (UnicodeDecodeError, AttributeError):
                    pass

        return data
