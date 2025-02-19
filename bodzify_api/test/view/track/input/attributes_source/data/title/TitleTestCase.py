from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase \
    import NonNullableStrFieldFromDataTestCase


class TitleTestCase(NonNullableStrFieldFromDataTestCase):
    post_field_key = PostFields.TITLE

    def test_value_then_ok(self):
        value = 'fr'
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == value
