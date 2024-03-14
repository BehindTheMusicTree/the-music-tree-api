#!/usr/bin/env python

from abc import abstractmethod
from typing import Optional
import pytest

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class RatingNotNoneTestCase(ApiViewTestCase):

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None):
        class_methods_names_to_implement = ['test_1_then_2',
                                            'test_2_then_4',
                                            'test_3_then_6',
                                            'test_4_then_8',
                                            'test_5_then_10']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        super().setUp(methods_names_to_implement=class_methods_names_to_implement)
