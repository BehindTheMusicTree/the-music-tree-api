from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TagTestCase(CriteriaTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__('tag-detail', 'tag-list', CriteriaTypePks.TAG, *args, **kwargs)

    def _retrieve_tag(self, uuid):
        return self._retrieve_criteria(uuid)

    def _get_tags(self, **kwargs):
        return super()._get_criterias(**kwargs)

    def _post_tag(self, **kwargs):
        return self._post_criteria(**kwargs)

    def _put_tag(self, uuid, **kwargs):
        return self._put_criteria(uuid, **kwargs)

    def _delete_tag(self, uuid):
        return self._delete_criteria(uuid)
