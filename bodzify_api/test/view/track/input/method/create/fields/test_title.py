#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ViewTestCase import ViewTestCase
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_povided_then_set_from_filename(self):
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert self.saved_lib_track.title == \
            ViewTestCase.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_NONE
