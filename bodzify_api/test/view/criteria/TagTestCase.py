from typing import Optional
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.criteria.children.tag.Tag import Tag
from bodzify_api.serializer.schema.model.criteria.output.Fields import Fields
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.criteria.Criteria import Criteria
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
        response = self.api_client.get(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response=response)
        return response

    def _get_tags(self, **kwargs):
        response = self.api_client.get(path=reverse(self.list_endpoint), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _post_tag(self, **kwargs):
        response = self.api_client.post(path=reverse(self.list_endpoint),
                                        data=kwargs,
                                        content_type='application/json')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_tag_attribute(response)
        return response

    def _put_tag(self, uuid: UUID, **kwargs):
        response = self.api_client.put(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
                                       data=kwargs,
                                       content_type='application/json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_tag_attribute(response)
        return response

    def _delete_tag(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
