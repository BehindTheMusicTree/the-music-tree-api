#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.LibTrackPostSchemaSerializer import FIELDS as POST_FIELDS


class TestCase(ApiViewTestCase):

    def test_without_a_file_and_a_title_then_ok(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Foire",
                  duration=0)
        data = {
            POST_FIELDS.TITLE: "Jobo"
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
