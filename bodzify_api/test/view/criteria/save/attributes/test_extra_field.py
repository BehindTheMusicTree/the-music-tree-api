#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_extra_field_then_error(self):
        data_dict = {"notExistingField": "Koko"}
        response = self.post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
