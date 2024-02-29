#!/usr/bin/env python

from abc import abstractmethod
import pytest

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class LibTrackFromFileMetadataRatingFieldTestCase(ApiViewTestCase):

    @abstractmethod
    def test_none_then_none(self):
        pass

    @abstractmethod
    def test_1_then_2(self):
        pass

    @abstractmethod
    def test_2_then_4(self):
        pass

    @abstractmethod
    def test_3_then_6(self):
        pass

    @abstractmethod
    def test_4_then_8(self):
        pass

    @abstractmethod
    def test_5_then_10(self):
        pass
