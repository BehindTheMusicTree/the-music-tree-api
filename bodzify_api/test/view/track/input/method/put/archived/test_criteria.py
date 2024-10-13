#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_archived_lib_track_then_criteria_has_plus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo")
        self.model_fixture_factory.create_lib_track(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="archived 1", genre=criteria, archived=True)
        track_love = self.model_fixture_factory.create_lib_track(title="Love", genre=criteria)
        data = {PutFields.ARCHIVED: "true"}
        response = self.put_lib_track(lib_track_uuid=track_love.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.criteria.lib_tracks_archived_count == 2  # type: ignore

    def test_unarchived_then_criteria_has_minus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo", lib_tracks_archived_count=True)
        self.model_fixture_factory.create_lib_track(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_lib_track(title="archived 1", genre=criteria, archived=True)
        track = self.model_fixture_factory.create_lib_track(title="Love", genre=criteria, archived=True)
        data = {PutFields.ARCHIVED: "false"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.lib_track_saved.criteria.lib_tracks_archived_count == 1  # type: ignore
