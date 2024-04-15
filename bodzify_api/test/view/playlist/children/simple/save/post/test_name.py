#!/usr/bin/env python

from rest_framework import status
from bodzify_api.serializer.playlist.children.simple.input.schema.SimplePlaylistSaveSchemaSerializer import FIELDS
from bodzify_api.test.view.playlist.children.simple.SimplePlaylistTestCase import SimplePlaylistTestCase


class TestCase(SimplePlaylistTestCase):

    def test_value_then_ok(self):
        data = {FIELDS.NAME: "a"}
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

    def test_empty_then_error(self):
        data = {FIELDS.NAME: ""}
        response = self.post_simple_playlist(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_not_provided_then_error(self):
        response = self.post_simple_playlist(data_dict={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
