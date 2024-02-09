#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_empty_then_none(self):
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: ""
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == None

    def test_existing(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: rock_genre.uuid
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_genre.parent == rock_genre

    def test_error_when_not_existing(self):
        rock_genre = G(Criteria,
            name="Rock",
            user=self.test_user,
            type=CriteriaTypesId.GENRE)
        data = {
            CRITERIA_ATTRIBUTES_LABEL.NAME: "Punk",
            CRITERIA_ATTRIBUTES_LABEL.PARENT: "not existing"
        }
        response = self.post_genre(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
