#!/usr/bin/env python

from abc import abstractmethod
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class LibTrackAttributeFromDataTestCase(ApiViewTestCase):

    @abstractmethod
    def test_not_empty_then_ok(self):
        pass

    @abstractmethod
    def test_empty_then_ok(self):
        pass

    @abstractmethod
    def test_null_then_ok(self):
        pass
