#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.track.input.endpoint.extract import Fields as ExtractFields
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        artist_name = "a" * settings.ARTIST_NAME_LEN_MAX
        data = {ExtractFields.ARTIST_NAME: artist_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.artist is not None
        assert self.lib_track_saved.artist.name == artist_name

    def test_too_long_then_error(self):
        artist_name = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)
        data = {ExtractFields.ARTIST_NAME: artist_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {ExtractFields.ARTIST_NAME: ''}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.artist == None

    def test_existing(self):
        artist_name = "Kopoe"
        self.model_fixture_factory.create_artist(name=artist_name)
        data = {ExtractFields.ARTIST_NAME: artist_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.artist is not None
        assert self.lib_track_saved.artist.name == artist_name

    def test_not_existing(self):
        artist_name = "hoho"
        data = {ExtractFields.ARTIST_NAME: artist_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.artist is not None
        assert self.lib_track_saved.artist.name == artist_name
