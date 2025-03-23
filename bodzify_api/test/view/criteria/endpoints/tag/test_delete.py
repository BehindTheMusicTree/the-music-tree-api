from rest_framework import status

from bodzify_api.model.criteria.children.tag.Tag import Tag
from bodzify_api.test.view.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):

    def test_delete_then_405(self):
        tag = self.model_fixture_factory.create_tag(name='Sport')

        response = self._delete_tag(uuid=tag.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Tag.objects.filter(uuid=tag.uuid).count() == 0
