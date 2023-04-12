#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL


class TestCase(ApiViewTestCase):

    def test_parentNoneWhenNoParentProvided(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedGenre.parent.name == None
