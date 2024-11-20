from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from bodzify_api.filter.set.private_unique_resource.PrivateUniqueResourceFilterSet import PrivateUniqueResourceFilterSet
from bodzify_api.model.play.Play import Fields, Play
from bodzify_api.serializer.schema.model.play.input.schema.endpoint.post import PlayPostSerializer
from bodzify_api.serializer.schema.model.play.output.detailed import PlayDetailedSerializer
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet


class PlayViewSet(AppModelViewSet[Play]):
    def __init__(self, **kwargs):
        super().__init__(model_class=Play,
                         filterset_class=PrivateUniqueResourceFilterSet,
                         detailed_serializer_class=PlayDetailedSerializer,
                         create_serializer_class=PlayPostSerializer,
                         **kwargs)

    def get_queryset(self):
        return Play.objects.filter(user=self.request.user).order_by(f"-{Fields.CREATED_ON} ")

    def list(self, request: Request, *args, **kwargs) -> Response:
        return self._handle_list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return self._handle_retrieve(request, *args, **kwargs)

    # @transaction.atomic not needed
    @extend_schema(request=PlayPostSerializer, responses=PlayDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request, *args, **kwargs)
