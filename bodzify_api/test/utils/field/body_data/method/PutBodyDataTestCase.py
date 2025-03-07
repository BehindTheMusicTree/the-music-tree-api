

from bodzify_api.test.utils.AppTestCase import AppTestCase


class PutBodyDataTestCase(AppTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:
        class_methods_names_to_implement = ['test_not_provided_then_unchanged', 'test_provided_then_update']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
