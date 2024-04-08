#!/usr/bin/env python

from rest_framework import status
from ddf import G

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.utils import to_camel_case
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS


class TestCase(TrackTestCase):

    def test_title_in_both_then_take_data(self):
        data_title = "Rock"
        data_dict = {POST_FIELDS.TITLE: data_title}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.title == data_title  # type: ignore
