from rest_framework import status

from bodzify_api.serializer.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):

    def test_ok(self):
        tag = self.model_fixture_factory.create_tag(name="Sport")

        tag_new_name = "Kitchen"
        response = self._put_tag(uuid=tag.uuid, **{PutFields.NAME_PUBLIC: tag_new_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == tag_new_name
