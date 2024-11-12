from rest_framework import status

from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_extra_field_then_error(self):
        data_dict = {"notExistingField": "Koko"}
        response = self._post_genre(data_dict=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
