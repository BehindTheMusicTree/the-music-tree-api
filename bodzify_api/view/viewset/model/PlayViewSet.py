from django.db import transaction
from drf_spectacular.utils import extend_schema

from bodzify_api.model.play.Play import Fields, Play
from bodzify_api.serializer.schema.play.input.schema.endpoint.post import PlayPostSerializer
from bodzify_api.serializer.schema.play.output.detailed import PlayDetailedSerializer
from bodzify_api.service.PlayService import PlayService
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet


class PlayViewSet(AppModelViewSet[Play]):
    def __init__(self, **kwargs):
        super().__init__(
            service=PlayService(),
            model_class=Play,
            detailed_serializer_class=PlayDetailedSerializer,
            create_serializer_class=PlayPostSerializer,
            **kwargs
        )

    def get_queryset(self):
        return Play.objects.filter(
            user=self.request.user).order_by(
            f"-{Fields.TIME} ")

    @transaction.atomic
    @extend_schema(request=PlayPostSerializer, responses=PlayDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request, *args, **kwargs)
