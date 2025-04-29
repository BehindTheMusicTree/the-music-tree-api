from django.conf import settings
import json
import os
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet
from bodzify_api.serializer.model.criteria.input.tree_import import CriteriaTreeImportSerializer


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)

    @action(detail=False, methods=['post'])
    def load_reference_tree(self, request):
        try:
            # Load the static genre tree file
            static_path = os.path.join(settings.STATIC_ROOT, 'data', 'genre_reference_tree.json')
            with open(static_path, 'r') as f:
                data = json.load(f)

            # Validate the data using the serializer
            serializer = CriteriaTreeImportSerializer(data={'tree': data['tree']})
            serializer.is_valid(raise_exception=True)

            # Import the tree
            Genre.objects.import_criteria_tree(request.user, serializer.validated_data)

            # Return success response
            return Response({"message": "Reference genre tree loaded successfully"}, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            return Response({"error": "Reference genre tree file not found"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format in genre tree file"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
