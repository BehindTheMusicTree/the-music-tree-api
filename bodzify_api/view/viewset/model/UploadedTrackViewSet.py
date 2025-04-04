import os
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from bodzify_api.filtering.set.uploaded_track.UploadedTrackFilterSet import UploadedTrackFilterSet
from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.model.uploaded_track.Fields import Fields
from bodzify_api.view.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer
from bodzify_api.view.serializer.model.uploaded_track.input.post.post import UploadedTrackPostSerializer
from bodzify_api.view.serializer.model.uploaded_track.put.put import UploadedTrackPutSerializer
from bodzify_api.view.serializer.model.uploaded_track.output.simple import UploadedTrackSimpleSerializer
from bodzify_api.view.viewset.base.BaseViewSet import BaseViewSet


class UploadedTrackViewSet(BaseViewSet):
    """ViewSet for managing uploaded tracks."""

    queryset = UploadedTrack.objects.all()
    serializer_class = UploadedTrackSimpleSerializer
    filterset_class = UploadedTrackFilterSet

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UploadedTrackDetailedSerializer
        elif self.action == 'create':
            return UploadedTrackPostSerializer
        elif self.action in ['update', 'partial_update']:
            return UploadedTrackPutSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the track file."""
        track = self.get_object()
        return Response({
            Fields.FILE_PATH: track.file_path
        }, status=status.HTTP_200_OK)

    @extend_schema(request=UploadedTrackPostSerializer, responses=UploadedTrackDetailedSerializer)
    def create(self, request, *args, **kwargs):
        try:
            return self._handle_post(request)
        except Exception as e:
            if request.FILES.get(
                    Fields.TRACK_FILE_PUBLIC) and hasattr(
                    request.FILES[Fields.TRACK_FILE_PUBLIC],
                    'temporary_file_path'):
                try:
                    os.unlink(request.FILES[Fields.TRACK_FILE_PUBLIC].temporary_file_path())
                except (OSError, AttributeError):
                    pass
            raise

    @extend_schema(parameters=[
        OpenApiParameter(name=Fields.TITLE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=Fields.ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=Fields.ALBUM_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=Fields.GENRE_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=Fields.LANGUAGE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @extend_schema(request=UploadedTrackPutSerializer, responses=UploadedTrackDetailedSerializer)
    def update(self, request, *args, **kwargs):
        return self._handle_update(request)

    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
