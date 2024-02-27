#!/usr/bin/env python

from abc import abstractmethod
import pytest
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class AttributeFromFileMetadataTestCase(ApiViewTestCase):

    @abstractmethod
    def test_none_then_none(self):
        pass

    @abstractmethod
    def test_longest(self):
        pass
