#!/usr/bin/env python

from rest_framework import status
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_so_parent_none(self):
        genre_name = "Rock"
        data = {POST_FIELDS.GENRE_NAME: genre_name}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.parent == None  # type: ignore
