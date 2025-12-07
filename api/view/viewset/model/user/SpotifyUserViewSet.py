from drf_spectacular.utils import extend_schema

from api.model.user.spotify.SpotifyUser import SpotifyUser
from api.serializer.model.user.spotify.output.detailed import SpotifyUserDetailedSerializer
from api.view.viewset.model.AppModelViewSet import AppModelViewSet
from api.utils.decorators.spotify import spotify_user_required


class SpotifyUserViewSet(AppModelViewSet[SpotifyUser]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=SpotifyUser,
            detailed_serializer_class=SpotifyUserDetailedSerializer,
            is_private_resource=False,
            is_pk_uuid=False,
            **kwargs
        )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().filter(id=self.request.user.id)

    @extend_schema(
        description="Get the current user's Spotify profile",
        responses={
            200: SpotifyUserDetailedSerializer,
            401: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            },
            403: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    )
    @spotify_user_required
    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()
