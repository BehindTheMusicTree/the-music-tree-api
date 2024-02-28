#!/usr/bin/env python

from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as EXTRACT_FIELDS
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from rest_framework import status


class AttributeFromDataTestCase(ApiViewTestCase):
    extract_field_key = None

    def _test_ok(self, value):
        data = {
            self.extract_field_key: value
        }
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension='mp3', data_json=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore

    def test_not_empty_then_ok(self):
        self._test_ok("a")

    def test_empty_then_ok(self):
        self._test_ok("")


class ArtistTestCase(AttributeFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.ARTIST_NAME


class GenreTestCase(AttributeFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.GENRE_NAME


class LanguageTestCase(AttributeFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.LANGUAGE


class TitleTestCase(AttributeFromDataTestCase):
    extract_field_key = EXTRACT_FIELDS.TITLE
