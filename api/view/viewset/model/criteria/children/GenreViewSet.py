from django.conf import settings
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet
from api.serializer.model.criteria.input.tree_import import CriteriaTreeImportSerializer


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)

    @action(detail=False, methods=['post'], url_path='tree/load-reference')
    def load_reference_tree(self, request):
        data_path = settings.DATA_DIR / 'genre_reference_tree.json'

        if not data_path.exists():
            raise FileNotFoundError(f"Reference genre tree file not found at {data_path}")

        with open(data_path, 'r') as f:
            data = json.load(f)

        serializer = CriteriaTreeImportSerializer(data={'tree': data['tree']})
        serializer.is_valid(raise_exception=True)

        from api.model.uploaded_track.UploadedTrack import UploadedTrack
        from api.model.uploaded_track.Fields import Fields as UploadedTrackFields
        UploadedTrack.objects.filter(user=request.user).update(**{UploadedTrackFields.GENRE: None})

        Genre.objects.import_criteria_tree(request.user, serializer.validated_data)

        return Response({"message": "Reference genre tree loaded successfully"}, status=status.HTTP_201_CREATED)
