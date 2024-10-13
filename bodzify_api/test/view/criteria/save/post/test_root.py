#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.criteria.input.schema.endpoint.post import \
    Fields as PostFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_parent_not_provided_then_root_itself(self):
        data_dict = {PostFields.NAME: "Rock"}
        response = self.post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.root == self.saved_genre
