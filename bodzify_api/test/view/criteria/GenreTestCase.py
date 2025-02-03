from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class GenreTestCase(CriteriaTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__('genre-detail', 'genre-list', CriteriaTypePks.GENRE, *args, **kwargs)

    def _retrieve_genre(self, uuid):
        return self._retrieve_criteria(uuid)

    def _get_genres(self, **kwargs):
        return super()._get_criterias(**kwargs)

    def _post_genre(self, **kwargs):
        return self._post_criteria(**kwargs)

    def _put_genre(self, uuid, **kwargs):
        return self._put_criteria(uuid, **kwargs)

    def _delete_genre(self, uuid):
        return self._delete_criteria(uuid)
