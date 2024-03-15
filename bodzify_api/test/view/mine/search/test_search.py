#!/usr/bin/env python

from bodzify_api.test.ApiTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_ok(self):
        assert True == True
        # self.search_mine('youtube', "JUL")
