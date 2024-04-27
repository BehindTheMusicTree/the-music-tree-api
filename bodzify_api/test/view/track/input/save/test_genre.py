#!/usr/bin/env python

from rest_framework import status
from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LENGTH_MAX
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == genre_name

    def test_too_long_then_error(self):
        genre_name = "a" * (settings.CRITERIA_NAME_LENGTH_MAX + 1)
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {POST_FIELDS.GENRE_NAME: ''}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre == None

    def test_existing(self):
        genre_name = "Kopoe"
        self.model_fixture_factory.create_genre(name=genre_name)
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == genre_name

    def test_not_existing(self):
        genre_name = "hoho"
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == genre_name

    def test_new_so_parent_none(self):
        genre_name = "Rock"
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.parent == None
