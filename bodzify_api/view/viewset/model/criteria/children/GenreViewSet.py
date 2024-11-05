from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)
