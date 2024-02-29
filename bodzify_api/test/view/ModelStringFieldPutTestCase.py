#!/usr/bin/env python

from abc import abstractmethod
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class ModelStringFieldPutViewTestCase(ApiViewTestCase):

    @abstractmethod
    def test_not_provided_then_unchanged(self):
        pass

    @abstractmethod
    def test_none_then_none(self):
        pass

    @abstractmethod
    def test_empty_then_none(self):
        pass

    @abstractmethod
    def test_not_none_then_update(self):
        pass
