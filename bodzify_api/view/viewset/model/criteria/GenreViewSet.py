from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet
from django.db.models import Q


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(service=GenreService(), **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(type_id=CriteriaTypesId.GENRE)
        return filtered_queryset

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = self.model_class.objects.filter(user=self.request.user, type_id=CriteriaTypesId.GENRE)
        return queryset.get(**filter_kwargs)
