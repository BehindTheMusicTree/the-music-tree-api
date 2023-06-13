#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api import settings


class TestCase(ApiViewTestCase):
    
    def test_longestName(self):
        genreName = "a" * settings.CRITERIA_NAME_MAX_CHAR
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: genreName
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedGenre.name == genreName
    
    def test_errorWhenNameTooLong(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "a" * (settings.CRITERIA_NAME_MAX_CHAR + 1)
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_withExistingParent(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Rock"
        }
        self.postGenre(dataJson=data)
        rockGenre = self.savedGenre
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Hard rock",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rockGenre.uuid
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedGenre.parent.uuid == rockGenre.uuid
    
    def test_errorWhenNotExistingParent(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Hard rock",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: "notexisting"
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_errorWhenExtraField(self):
        data = {
            "notExistingField": "Koko"
        }
        response = self.postGenre(dataJson=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST