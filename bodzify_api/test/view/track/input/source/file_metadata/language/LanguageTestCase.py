#!/usr/bin/env python

import logging
from bodzify_api import settings
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSaveSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.test.view.track.input.source.file_metadata.AttributeFromFileMetadataTestCase \
    import AttributeFromFileMetadataTestCase
from rest_framework import status

logger = logging.getLogger('bodzify_api')


class LanguageTestCase(AttributeFromFileMetadataTestCase):
    save_field = SAVE_SCHEMA_FIELDS.LANGUAGE
    metadata_dict_key = AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE,
    length_max = settings.LIB_TRACK_LANGUAGE_LENGTH_MAX
    file_extension = None

    def test_none_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags(generic_sample_extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == None

    def test_longest(self):
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(
            generic_sample_extension=self.file_extension)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == 'a' * self.length_max


class LanguageMp3TestCase(LanguageTestCase):
    file_extension = 'mp3'


class LanguageFlacTestCase(LanguageTestCase):
    file_extension = 'flac'


class LanguageWavTestCase(LanguageTestCase):
    file_extension = 'wav'
