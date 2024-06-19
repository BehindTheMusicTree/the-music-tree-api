#!/usr/bin/env python

from typing import Optional

from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS


class ApiTestCase(AppTestCase):

    def setUp(self, methods_names_to_implement: Optional[list[str]] = None):
        super().setUp()
        if methods_names_to_implement is not None:
            for method_name in methods_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")

    @staticmethod
    def _merge_two_dicts(dict1, dict2):
        dict1.update(dict2)
        return dict1

    @staticmethod
    def _replace_none_values_by_empty_string(data_dict):
        if data_dict is None:
            return {}
        return {k: ('' if v is None else v) for k, v in data_dict.items()}

    def _set_results_attributes(self, response):
        self.results = response.json()[PAGINATED_RESPONSE_FIELDS.RESULTS]
        self.overall_total = response.json()[PAGINATED_RESPONSE_FIELDS.OVERALL_TOTAL]

    def _set_result(self, response):
        self.result = response.json()
