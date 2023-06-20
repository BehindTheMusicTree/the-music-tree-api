#!/usr/bin/env python
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_ok(self, query):
        return self.searchMine('youtube', query)
