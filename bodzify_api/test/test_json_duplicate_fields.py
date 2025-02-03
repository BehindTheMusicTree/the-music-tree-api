
from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as CriteriaPostFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_duplicate_fields_on_content_type_json_then_400(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{
            CriteriaPostFields.NAME_PUBLIC: "test",
            CriteriaPostFields.NAME_PUBLIC: "test2"
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
