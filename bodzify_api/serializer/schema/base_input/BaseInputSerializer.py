from typing import Counter
from rest_framework import serializers


class BaseInputSerializer(serializers.Serializer):

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())  # type: ignore
            if unknown_keys:
                raise serializers.ValidationError({"Unknown fields": "{}".format(unknown_keys)})

        field_names = list(data.keys())
        field_counts = Counter(field_names)
        duplicates = [field for field, count in field_counts.items() if count > 1]
        if duplicates:
            raise serializers.ValidationError({
                'error': f'Duplicate fields found: {", ".join(duplicates)}'
            })

        return super().validate(data)
