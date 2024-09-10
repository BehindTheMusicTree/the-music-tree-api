#!/usr/bin/env python

import uuid
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_with_9_matches_then_the_one_with_duration_field(self):
        response = self.post_lib_track_with_specific_sample("total_eclipse_9_matches_but_one_with_duration.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            '9f3c3b61-41a6-4bb9-a49c-33606f536784')

    def test_with_2_matches_then_the_one_with_closest_duration(self):
        response = self.post_lib_track_with_specific_sample("lorie_2_matches_but_one_with_closest_duration.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            '76e1d5e6-9713-4c6b-8238-9d7983fd4497')

    def test_with_2_matches_with_same_duration_and_same_number_of_fields_then_the_one_with_the_most_release_groups(self):
        response = self.post_lib_track_with_specific_sample(
            "allumerlefeu_2_matches_but_one_with_more_release_groups.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            '82b4c5fe-0980-4495-95b0-bd5e124486d8')

    def test_with_25_matches_then_select_the_one_with_best_duration_and_most_fields_and_most_release_groups(self):
        response = self.post_lib_track_with_specific_sample(
            "queen_25_matches_but_one_with_best_duration_and_most_fields_and_most_release_groups.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.musicbrainz_recording.uuid == uuid.UUID(  # type: ignore
            '3604eb06-4bc2-4416-9b31-ceadae51bc70')
