#!/usr/bin/env python

from abc import abstractmethod
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class StringFieldSaveTestCase(ApiViewTestCase):

    @abstractmethod
    def test_longest_then_ok(self):
        pass

    @abstractmethod
    def test_too_long_then_error(self):
        pass

    @abstractmethod
    def test_none_then_none(self):
        pass

    @abstractmethod
    def test_existing(self):
        pass

    @abstractmethod
    def test_not_existing(self):
        pass
