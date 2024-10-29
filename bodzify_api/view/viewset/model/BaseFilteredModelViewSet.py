from rest_framework.exceptions import ValidationError
from bodzify_api.constants.model_fields import ModelFields
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet

class BaseFilteredModelViewSet(AppModelViewSet):
    filter_class = None
    model_class = None

    def get_queryset(self):
        try:
            snake_case_params = self.get_dict_in_snake_case_keys_from_dict_in_camel_case_keys(self.request.GET)
            queryset = self.model_class.objects.filter(user=self.request.user)
            
            if self.filter_class:
                queryset = self.filter_class(snake_case_params, queryset=queryset).qs
            
            return queryset.order_by(f"-{ModelFields.CREATED_ON}")
        except ValidationError as e:
            raise ValidationError(e.detail)