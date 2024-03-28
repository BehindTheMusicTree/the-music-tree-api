#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackExtractSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LENGTH_MAX
        data = {EXTRACT_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.name == genre_name  # type: ignore

    def test_too_long_then_error(self):
        genre_name = "a" * (settings.CRITERIA_NAME_LENGTH_MAX + 1)
        data = {EXTRACT_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_empty_then_none(self):
        data = {EXTRACT_FIELDS.GENRE_NAME: ''}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre == None

    def test_existing(self):
        genre_name = "Kopoe"
        G(Criteria, user=self.test_user, name=genre_name, type=CRITERIA_TYPES_ID.GENRE)
        data = {EXTRACT_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.name == genre_name  # type: ignore

    def test_not_existing(self):
        genre_name = "hoho"
        data = {EXTRACT_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_lib_track.genre.name == genre_name  # type: ignore

    def test_new_so_parent_none(self):
        genre_name = "Rock"
        data = {EXTRACT_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.parent == None  # type: ignore
