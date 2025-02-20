

from bodzify_api.test.utils.field.filter.foreign_key.ForeignKeyFilterTestCase import ForeignKeyFilterTestCase


class PrivateForeignKeyFilterTestCase(ForeignKeyFilterTestCase):

    def setUp(self, allow_empty_value: bool, methods_names_to_implement=None):
        class_methods_to_implement = ['test_of_another_user_then_empty']
        if methods_names_to_implement:
            class_methods_to_implement += methods_names_to_implement
        return super().setUp(methods_names_to_implement=methods_names_to_implement, allow_empty_value=allow_empty_value)
