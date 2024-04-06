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
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS


class TestCase(TrackTestCase):

    def test_artist_in_both_then_take_data(self):
        data_artist_name = "Rock"
        data_dict = {POST_FIELDS.ARTIST_NAME: data_artist_name}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.artist.name == data_artist_name  # type: ignore
