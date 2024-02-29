#!/usr/bin/env python

from abc import abstractmethod
import pytest

from bodzify_api.test.view.track.input.source.file_metadata.rating.LibraryTrackFromFileMetadataRatingFieldTestCase \
    import LibTrackFromFileMetadataRatingFieldTestCase


@pytest.mark.django_db
class LibraryTrackFromFileMetadataRatingWithHalfFieldTestCase(LibTrackFromFileMetadataRatingFieldTestCase):

    @abstractmethod
    def test_0_then_0(self):
        pass

    @abstractmethod
    def test_0_and_half_then_1(self):
        pass

    @abstractmethod
    def test_1_and_half_then_3(self):
        pass

    @abstractmethod
    def test_2_and_half_then_5(self):
        pass

    @abstractmethod
    def test_3_and_half_then_7(self):
        pass

    @abstractmethod
    def test_4_and_half_then_9(self):
        pass
