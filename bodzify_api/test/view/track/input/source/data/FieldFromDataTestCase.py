#!/usr/bin/env python

from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class FieldFromDataTestCase(TrackTestCase):
    post_field_key = None

    def _test_ok(self, value):
        data = {self.post_field_key: value}
        response = self.post_lib_track_with_generic_sample_no_tags(extension='mp3', data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore


class FieldStrFromDataTestCase(FieldFromDataTestCase):

    def test_not_empty_then_ok(self):
        self._test_ok("a")

    def test_empty_then_ok(self):
        self._test_ok("")


class FieldIntFromDataTestCase(FieldFromDataTestCase):

    def test_not_empty_then_ok(self):
        self._test_ok(1)


class ArtistTestCase(FieldStrFromDataTestCase):
    post_field_key = POST_FIELDS.ARTIST_NAME


class GenreTestCase(FieldStrFromDataTestCase):
    post_field_key = POST_FIELDS.GENRE_NAME


class LanguageTestCase(FieldStrFromDataTestCase):
    post_field_key = POST_FIELDS.LANGUAGE


class TitleTestCase(FieldStrFromDataTestCase):
    post_field_key = POST_FIELDS.TITLE


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = POST_FIELDS.RATING
