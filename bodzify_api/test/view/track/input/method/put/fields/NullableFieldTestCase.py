from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class NullableFieldTestCase(LibTrackTestCase):

    def setUp(self):
        super().setUp(methods_names_to_implement=['test_not_provided_then_unchanged',
                                                  'test_empty_then_none',
                                                  'test_not_none_then_update'])
