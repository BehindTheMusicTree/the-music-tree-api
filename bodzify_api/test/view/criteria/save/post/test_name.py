#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPostSerializer import FIELDS as POST_FIELDS


class TestCase(CriteriaTestCase):

    def test_not_provided_then_error(self):
        response = self.post_genre(data_dict={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_empty_then_error(self):
        data = {POST_FIELDS.PARENT: ""}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_value_then_ok(self):
        name = "rock"
        data = {POST_FIELDS.NAME: name}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_genre.name == name
