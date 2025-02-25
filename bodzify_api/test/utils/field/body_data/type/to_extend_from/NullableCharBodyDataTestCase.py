
from bodzify_api.test.utils.field.body_data.type.base.NullableBodyDataTestCase import     NullableBodyDataTestCase


class NullableCharBodyDataTestCase(NullableBodyDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_value_then_ok']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement)
