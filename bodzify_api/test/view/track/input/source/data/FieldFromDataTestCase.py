#!/usr/bin/env python

from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from rest_framework import status


class FieldFromDataTestCase(ApiViewTestCase):
    extract_field_key = None

    def _test_ok(self, value):
        data = {
            self.extract_field_key: value
        }
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension='mp3', data_json=data)
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
    extract_field_key = EXTRACT_FIELDS.ARTIST_NAME


class GenreTestCase(FieldStrFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.GENRE_NAME


class LanguageTestCase(FieldStrFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.LANGUAGE


class TitleTestCase(FieldStrFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.TITLE


class RatingTestCase(FieldIntFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.RATING
