import inspect
import pkgutil
from pathlib import Path

from rest_framework import serializers

from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.serializer.PutSerializer import PutSerializer
from bodzify_api.test.utils.AppTestCase import AppTestCase


class TestInputSerializerInheritance(AppTestCase):
    """
    Test that all input serializers inherit from AppInputSerializer.

    AppInputSerializer provides input validation features:
    - Multipart form data normalization and validation
    - Duplicate field detection
    - Unknown field detection
    - List field handling with [] suffix for multipart requests
    - Consistent error handling using AppValidationException

    Output serializers (read-only, for API responses) do not need AppInputSerializer
    and are excluded from this test. Only input serializers (POST, PUT, etc.) are checked.
    """
    BASE_SERIALIZER_CLASSES = {AppInputSerializer, PutSerializer}

    def _is_input_serializer(self, modname: str, name: str) -> bool:
        """
        Check if a serializer is an input serializer (not output/read-only).

        Input serializers are those used for:
        - POST requests (creating resources)
        - PUT/PATCH requests (updating resources)
        - Input validation

        They are identified by:
        - Being in directories named "input/"
        - Having names containing: Post, Put, Create, Update, Input

        Output serializers (read-only, for GET responses) are excluded:
        - Those in "output/" directories
        - Named: *DetailedSerializer, *SimpleSerializer, *MinimumSerializer
        """
        modname_lower = modname.lower()
        name_lower = name.lower()

        # Exclude output serializers first (they're clearly read-only)
        is_output = (
            "/output/" in modname_lower
            or ".output." in modname_lower
            or modname_lower.endswith(".output")
        )

        if is_output:
            return False

        # Input serializers are in "input" directories
        is_in_input_dir = (
            "/input/" in modname_lower
            or ".input." in modname_lower
            or modname_lower.endswith(".input")
        )

        # Or have input-related names (Post, Put, Create, Update, Input)
        has_input_name = (
            "post" in name_lower
            or "put" in name_lower
            or "create" in name_lower
            or "update" in name_lower
            or "input" in name_lower
        )

        return is_in_input_dir or has_input_name

    def _discover_serializer_classes(self):
        """
        Discover all input serializer classes in the bodzify_api.serializer package.

        Returns:
            List of input serializer classes that should inherit from AppInputSerializer.
        """
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
                    # Exclude AppInputSerializer by name (safety check in case object identity fails)
                    if name == "AppInputSerializer":
                        continue
                    if (
                        name.endswith("Serializer")
                        and obj not in self.BASE_SERIALIZER_CLASSES
                        and issubclass(obj, (serializers.Serializer, serializers.ModelSerializer))
                        and obj.__module__ == modname
                        and self._is_input_serializer(modname, name)
                    ):
                        serializer_classes.append(obj)
            except (ImportError, AttributeError, TypeError):
                continue

        return serializer_classes

    def test_all_input_serializers_inherit_from_app_input_serializer(self):
        """
        Verify that all input serializers inherit from AppInputSerializer.

        This test ensures that all serializers used for input validation (POST, PUT, etc.)
        inherit from AppInputSerializer, which provides:
        - Multipart form data handling
        - Duplicate field detection
        - Unknown field detection
        - Consistent error handling

        Output serializers (read-only) are excluded from this check as they don't
        perform input validation and don't need AppInputSerializer.
        """
        serializer_classes = self._discover_serializer_classes()
        violations = []

        for serializer_class in serializer_classes:
            if AppInputSerializer not in serializer_class.__mro__:
                violations.append(
                    f"{serializer_class.__name__} ({serializer_class.__module__}) "
                    f"does not inherit from AppInputSerializer"
                )

        assert not violations, (
            f"Found {len(violations)} input serializer(s) that do not inherit from AppInputSerializer:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\n\nAll input serializers must inherit from AppInputSerializer (not DRF's Serializer directly). "
            + "Output serializers (read-only) do not need AppInputSerializer. "
            + "See DEVELOPMENT.md for details."
        )
