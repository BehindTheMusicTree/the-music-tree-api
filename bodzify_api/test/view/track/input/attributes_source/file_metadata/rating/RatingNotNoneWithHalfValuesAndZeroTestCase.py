
import pytest

from bodzify_api.test.view.track.input.attributes_source.file_metadata.rating.RatingNotNoneTestCase import \
    RatingNotNoneTestCase


@pytest.mark.django_db
class RatingNotNoneWithHalfValuesAndZeroTestCase(RatingNotNoneTestCase):

    def setUp(self):
        return super().setUp(methods_names_to_implement=['test_0_then_0',
                                                         'test_0_and_half_then_1',
                                                         'test_1_and_half_then_3',
                                                         'test_2_and_half_then_5',
                                                         'test_3_and_half_then_7',
                                                         'test_4_and_half_then_9'])
