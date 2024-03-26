#!/usr/bin/env python

from rest_framework import status
from ddf import G

from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.utils import to_camel_case
from bodzify_api.serializer.play.input.schema.PlayPostSchemaSerializer import FIELDS


class TestCase(PlayTestCase):

    def test_extra_field_then_error(self):
        data = {
            'nonExistingField': 'oifjqoif'
        }
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_non_existant_content_object_uuid_then_error(self):
        data = {
            to_camel_case(FIELDS.CONTENT_OBJECT_UUID): 'oifjqoif'
        }
        response = self.post_play(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
