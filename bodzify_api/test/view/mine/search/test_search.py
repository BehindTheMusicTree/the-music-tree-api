#!/usr/bin/env python

from bodzify_api.test.ApiTestCase import ApiTestCase


class TestCase(ApiTestCase):

    def test_ok(self):
        assert True == True
        # self.search_mine('youtube', "JUL")
