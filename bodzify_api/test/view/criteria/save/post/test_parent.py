#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.schema.criteria.input.schema.endpoint.post import \
    Fields as PostFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_not_provided_then_none(self):
        data = {PostFields.NAME: "Rock"}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_empty_then_none(self):
        data = {
            PostFields.NAME: "Rock",
            PostFields.PARENT: ""
        }
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None
