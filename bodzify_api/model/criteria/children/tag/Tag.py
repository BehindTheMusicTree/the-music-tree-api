from bodzify_api.model.criteria.Criteria import Criteria
from .TagManager import TagManager


class Tag(Criteria):

    objects: 'TagManager' = TagManager()

    class Meta:
        proxy = True
