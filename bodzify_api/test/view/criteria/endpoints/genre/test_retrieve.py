from uuid import UUID
from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields as RetrieveFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(GenreTestCase):

    def test_ok(self):
        name = 'rock'
        uuid = self.model_fixture_factory.create_genre(name=name).uuid
        response = self._retrieve_genre(uuid=uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name
