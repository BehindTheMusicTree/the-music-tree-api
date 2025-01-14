from bodzify_api.test.field.body_data.BodyDataTestCase import BodyDataTestCase


class NotNullableBodyDataTestCase(BodyDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_empty_then_error']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement)
