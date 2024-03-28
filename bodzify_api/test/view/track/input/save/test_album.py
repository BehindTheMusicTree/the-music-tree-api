#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.Album import Album
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackExtractSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LENGTH_MAX
        data = {EXTRACT_FIELDS.ALBUM_NAME: album_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.name == album_name  # type: ignore

    def test_too_long_then_error(self):
        album_name = "a" * (settings.ALBUM_NAME_LENGTH_MAX + 1)
        data = {EXTRACT_FIELDS.ALBUM_NAME: album_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_empty_then_none(self):
        data = {EXTRACT_FIELDS.ALBUM_NAME: ''}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album == None

    def test_existing(self):
        album_name = "Kopoe"
        G(Album, user=self.test_user, name=album_name)
        data = {EXTRACT_FIELDS.ALBUM_NAME: album_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.name == album_name  # type: ignore

    def test_not_existing(self):
        album_name = "hoho"
        data = {EXTRACT_FIELDS.ALBUM_NAME: album_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.name == album_name  # type: ignore
