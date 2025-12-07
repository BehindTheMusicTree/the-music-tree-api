from rest_framework import status

from api.model.criteria.Criteria import Fields
from api.test.integration.view.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):

    def test_ok(self):
        tag_name = "Sport"
        self.model_fixture_factory.create_tag(name=tag_name)

        response = self._list_tags()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        tag_json = self.results[0]
        assert tag_json[Fields.NAME_PUBLIC] == tag_name
