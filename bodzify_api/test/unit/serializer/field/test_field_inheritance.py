import inspect
import pkgutil
from pathlib import Path

from rest_framework import serializers

from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.test.utils.AppTestCase import AppTestCase


class TestFieldInheritance(AppTestCase):
    """
    Test that all fields used in serializers are AppField-based.

    AppField provides:
    - Consistent error handling using AppValidationException (for input validation)
    - Automatic error code mapping from DRF validation keys
    - Proper field name handling for list fields (with [] suffix)

    Note: AppField fields can be used in both input and output serializers.
    The validation error handling is only triggered during input validation.
    """
    BASE_FIELD_CLASSES = {AppField}

    # DRF base field classes that have AppField equivalents and should not be used directly
    DRF_BASE_FIELDS_WITH_APP_EQUIVALENTS = {
        'serializers.CharField': 'AppCharField',
        'serializers.BooleanField': 'AppBooleanField',
        'serializers.UUIDField': 'AppUuidField',
        'serializers.EmailField': 'AppEmailField',
        'serializers.URLField': 'AppUrlField',
        'serializers.FileField': 'AppFileField',
        'serializers.ListField': 'AppListField',
        'serializers.DictField': 'AppDictField',
    }

    # Fields that are acceptable for output serializers (read-only, no validation needed)
    # These are typically used in output serializers for computed/read-only fields
    ACCEPTABLE_DRF_FIELDS = {
        'serializers.IntegerField',  # Used for counts, IDs in output serializers
        'serializers.FloatField',
        'serializers.DecimalField',
        'serializers.DateTimeField',
        'serializers.DateField',
        'serializers.TimeField',
        'serializers.DurationField',
        'serializers.ChoiceField',
        'serializers.MultipleChoiceField',
        'serializers.SlugField',
        'serializers.IPAddressField',
        'serializers.JSONField',
        'serializers.SerializerMethodField',  # Read-only computed fields
        'rest_framework.fields.IntegerField',
        'rest_framework.fields.SerializerMethodField',
    }

    def _discover_serializer_classes(self):
        """Discover all serializer classes in the bodzify_api.serializer package."""
        serializer_classes = []
        serializer_package_path = Path(__file__).parent.parent.parent.parent / "serializer"

        for importer, modname, ispkg in pkgutil.walk_packages(
            path=[str(serializer_package_path)],
            prefix="bodzify_api.serializer."
        ):
            if ispkg or modname.endswith(".Fields") or "test" in modname:
                continue

            try:
                module = __import__(modname, fromlist=[""])
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        name.endswith("Serializer")
                        and issubclass(obj, (serializers.Serializer, serializers.ModelSerializer))
                        and obj.__module__ == modname
                    ):
                        serializer_classes.append((modname, name, obj))
            except (ImportError, AttributeError, TypeError):
                continue

        return serializer_classes

    def _is_output_serializer(self, modname: str, serializer_name: str) -> bool:
        """Check if a serializer is an output serializer (read-only)."""
        modname_lower = modname.lower()
        name_lower = serializer_name.lower()
        return (
            "/output/" in modname_lower
            or ".output." in modname_lower
            or modname_lower.endswith(".output")
            or "detailed" in name_lower
            or "simple" in name_lower
            or "minimum" in name_lower
        )

    def _get_field_classes_from_serializer(self, serializer_class):
        """Extract field classes used in a serializer."""
        field_classes = []
        for field_name, field in serializer_class._declared_fields.items():
            field_class = field.__class__
            field_classes.append((field_name, field_class))
        return field_classes

    def test_all_used_fields_are_app_field_based(self):
        """
        Verify that all fields used in serializers are AppField-based.

        This test ensures that serializers use AppField-based fields (like AppCharField,
        AppListField, etc.) instead of DRF's base fields directly (like serializers.CharField).

        Fields are used in both input and output serializers, so all fields
        should be AppField-based to ensure consistent error handling.
        """
        serializer_classes = self._discover_serializer_classes()
        violations = []

        for modname, serializer_name, serializer_class in serializer_classes:
            field_classes = self._get_field_classes_from_serializer(serializer_class)
            is_output = self._is_output_serializer(modname, serializer_name)

            for field_name, field_class in field_classes:
                field_class_name = f"{field_class.__module__}.{field_class.__name__}"

                # For output serializers, allow IntegerField for computed fields (counts, etc.)
                if is_output and field_class_name in {'serializers.IntegerField', 'rest_framework.fields.IntegerField'}:
                    continue

                # Skip other acceptable fields (typically used in output serializers)
                if field_class_name in self.ACCEPTABLE_DRF_FIELDS:
                    continue

                # Check if it's a DRF base field that has an AppField equivalent
                if field_class_name in self.DRF_BASE_FIELDS_WITH_APP_EQUIVALENTS:
                    app_equivalent = self.DRF_BASE_FIELDS_WITH_APP_EQUIVALENTS[field_class_name]
                    violations.append(
                        f"{serializer_name}.{field_name} uses {field_class_name} "
                        f"(should use {app_equivalent} instead)"
                    )
                # Check if it's a custom field that doesn't inherit from AppField
                elif (field_class.__module__.startswith('bodzify_api.serializer.field')
                      and AppField not in field_class.__mro__
                      and field_class not in self.BASE_FIELD_CLASSES):
                    violations.append(
                        f"{serializer_name}.{field_name} uses {field_class_name} "
                        f"which does not inherit from AppField"
                    )

        assert not violations, (
            f"Found {len(violations)} field(s) that are not AppField-based:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\n\nAll fields used in serializers must be AppField-based "
            + "(e.g., AppCharField instead of serializers.CharField). "
            + "See DEVELOPMENT.md for details."
        )
