#!/usr/bin/env python

import logging
from bodzify_api import AudioMetadataManager
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SAVE_FIELDS
from bodzify_api.test.view.track.input.update_file_metadata.UpdateFileMetadataIntTestCase import \
    UpdateFileMetadataIntTestCase


logger = logging.getLogger('bodzify_api')


class UpdateFileMetadataRatingTestCase(UpdateFileMetadataIntTestCase):

    save_field = SAVE_FIELDS.RATING
    metadata_dict_key = AudioMetadataManager.METADATA_DICT_KEYS.RATING
    value_min = 0
    value_max = 10
    value_min_in_metadata = 0
