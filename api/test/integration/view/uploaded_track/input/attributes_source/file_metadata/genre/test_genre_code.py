
from typing import cast
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_genre_code_from_riff_then_genre_name(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.GENRE_CODE_ID3V1_ABSTRACT_MP3, title='genre code abstract')

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        genre = cast(Genre, self.saved_object.genre)
        assert genre.name == 'Christmas'

    def test_genre_code_unknown_from_riff_then_None(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.GENRE_CODE_ID3V1_UNKNOWN_MP3, title='genre code unknown')

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
