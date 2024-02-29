#!/usr/bin/env python

from abc import abstractmethod
import pytest

from bodzify_api.test.view.track.input.source.file_metadata.rating.LibTrackFromFileMetadataRatingTestCase \
    import LibTrackFromFileMetadataRatingFieldTestCase


@pytest.mark.django_db
class LibTrackFromFileMetadataRatingWithHalfValuesTestCase(LibTrackFromFileMetadataRatingFieldTestCase):

    def setUp(self):
        return super().setUp(methodes_names_to_implenent=['test_0_then_0',
                                                          'test_0_and_half_then_1',
                                                          'test_1_and_half_then_3',
                                                          'test_2_and_half_then_5',
                                                          'test_3_and_half_then_7',
                                                          'test_4_and_half_then_9'])
