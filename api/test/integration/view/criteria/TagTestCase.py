from uuid import UUID

from django.urls import reverse

from api.model.criteria.children.tag.Tag import Tag
from api.serializer.model.criteria.output.Fields import Fields
from api.test.utils.AppTestCase import AppTestCase


class TagTestCase(AppTestCase[Tag]):
    model_class = Tag
    saved_object: Tag

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = 'tag-detail'
        self.list_endpoint = 'tag-list'

    def _retrieve_tag(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}), handle_response=self._set_results)

    def _list_tags(self, **kwargs):
        return self.api_client.get(
            path=reverse(self.list_endpoint), data=kwargs, handle_response=self._set_results)

    def _post_tag(self, **kwargs):
        return self.api_client.post(path=reverse(self.list_endpoint),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _put_tag(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_tag(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))
