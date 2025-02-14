from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.criteria.children.tag.Tag import Tag
from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields
from bodzify_api.test.ApiTestCase import ApiTestCase


class TagTestCase(ApiTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = 'tag-detail'
        self.list_endpoint = 'tag-list'

    def _set_saved_tag_attribute(self, response):
        uuid = response.json()[Fields.UUID]
        self.saved_tag = Tag.objects.get(user=self.test_user1, uuid=uuid)

    def _retrieve_tag(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            on_success=self._set_result
        )

    def _get_tags(self, **kwargs):
        return self.api_client.get(
            path=reverse(self.list_endpoint),
            data=kwargs,
            on_success=self._set_results_attributes
        )

    def _post_tag(self, **kwargs):
        return self.api_client.post(
            path=reverse(self.list_endpoint),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_tag_attribute
        )

    def _put_tag(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_tag_attribute
        )

    def _delete_tag(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
