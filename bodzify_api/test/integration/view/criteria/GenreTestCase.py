from uuid import UUID

from django.urls import reverse

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.utils.AppTestCase import AppTestCase


class GenreTestCase(AppTestCase[Genre]):
    saved_object: Genre
    model_class = Genre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = 'genre-detail'
        self.list_endpoint = 'genre-list'

    def _retrieve_genre(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={'pk': uuid}), handle_response=self._set_results)

    def _list_genres(self, **kwargs):
        return self.api_client.get(path=reverse(self.list_endpoint), data=kwargs, handle_response=self._set_results)

    def _get_genres_tree(self):
        return self.api_client.get(path=reverse(self.list_endpoint) + 'tree/',
                                   handle_response=self._set_error_response_result_if_failure)

    def _post_genre(self, **kwargs):
        return self.api_client.post(path=reverse(self.list_endpoint),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _post_genre_with_duplicate_fields(self, raw_json: str):
        return self.api_client.post(path=reverse(self.list_endpoint),
                                    data=raw_json,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _put_genre(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _put_genre_with_duplicate_fields(self, uuid: UUID, raw_json: str):
        return self.api_client.put(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}),
                                   data=raw_json,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_genre(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={'pk': uuid}))

    def _post_genres_tree_import(self, data=None):
        return self.api_client.post(path=reverse(self.list_endpoint) + 'tree/import/',
                                    data=data,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _post_genres_tree_load_reference(self):
        return self.api_client.post(path=reverse(self.list_endpoint) + 'tree/load-reference/',
                                    content_type='application/json',
                                    handle_response=self._set_error_response_result_if_failure)
