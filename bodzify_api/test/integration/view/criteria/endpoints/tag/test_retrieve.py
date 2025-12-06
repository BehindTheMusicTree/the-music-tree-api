from rest_framework import status

from bodzify_api.serializer.model.criteria.output.Fields import Fields as RetrieveFields
from bodzify_api.test.integration.view.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):

    def test_ok(self):
        name = 'Sport'
        uuid = self.model_fixture_factory.create_tag(name=name).uuid

        response = self._retrieve_tag(uuid=uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name
