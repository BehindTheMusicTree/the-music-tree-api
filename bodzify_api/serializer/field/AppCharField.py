from rest_framework import serializers


class AppCharField(serializers.CharField):
    def run_validation(self, data):
        if isinstance(data, (list, tuple)) and len(data) == 2:
            return data[0]
        return super().run_validation(data)
