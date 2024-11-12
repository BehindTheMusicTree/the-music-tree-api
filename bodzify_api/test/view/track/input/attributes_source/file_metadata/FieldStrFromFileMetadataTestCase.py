import pytest

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class FieldStrNullableFromFileMetadataTestCase(LibTrackTestCase):

    def setUp(self):
        super().setUp(methods_names_to_implement=['test_none_then_none', 'test_longest'])
