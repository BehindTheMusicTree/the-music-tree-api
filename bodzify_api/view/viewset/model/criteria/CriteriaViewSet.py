from django.db import transaction
from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import OpenApiParameter, extend_schema  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore

from bodzify_api.filtering.set.criteria.Fields import Fields as FilterFields
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.criteria.input.post import CriteriaPostSerializer
from bodzify_api.serializer.model.criteria.input.put import CriteriaPutSerializer
from bodzify_api.serializer.model.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.serializer.model.criteria.output.simple import CriteriaSimpleSerializer

from ..base.AppModelViewSet import AppModelViewSet


class CriteriaViewSet(AppModelViewSet[Criteria]):
    def __init__(self, model_class: type[Criteria], **kwargs):
        # Filtersets must be imported after Django is loaded
        from bodzify_api.filtering.set.criteria.CriteriaFilterSet import CriteriaFilterSet
        super().__init__(model_class=model_class,
                         filterset_class=CriteriaFilterSet,
                         simple_serializer_class=CriteriaSimpleSerializer,
                         detailed_serializer_class=CriteriaDetailedSerializer,
                         create_serializer_class=CriteriaPostSerializer,
                         update_serializer_class=CriteriaPutSerializer,
                         **kwargs)

    @transaction.atomic
    @extend_schema(request=CriteriaPostSerializer, responses=CriteriaDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request)

    @transaction.atomic
    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a criteria.

        When deleting a criteria:
        - If it has children and a parent, children are reassigned to the parent
        - If it has children but no parent, children become root criteria
        - If it's a root criteria, tracks are moved to the criterialess playlist
        - The criteria playlist is deleted along with the criteria
        """
        criteria = self.get_object()
        is_root = criteria.is_root

        # Handle tracks transfer for root criteria
        if is_root:
            # Get the criterialess playlist for this criteria type
            criterialess_playlist = CriteriaPlaylist.objects.filter(
                user=criteria.user,
                criteria=None,
                type=criteria.type
            ).first()

            if criterialess_playlist and hasattr(criteria, 'criteria_playlist'):
                # Get tracks from criteria and its descendants
                criteria_playlist = criteria.criteria_playlist

                # Get all lib_track_playlist_rels from the playlist
                lib_track_rels = list(criteria_playlist.lib_track_playlist_rels.all().order_by('position'))

                # Add tracks to criterialess playlist in first positions
                from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel

                for rel in lib_track_rels:
                    # Create new relationship for criterialess playlist
                    LibTrackPlaylistRel(
                        user=criteria.user,
                        playlist=criterialess_playlist,
                        lib_track=rel.lib_track
                    ).save()

        # Handle children reassignment before deletion
        if criteria.children.exists():
            children = list(criteria.children.all())
            if criteria.parent:
                # Reassign children to grandparent
                for child in children:
                    child.parent = criteria.parent
                    child.save(update_fields=['parent_id'])
            else:
                # Make children root criteria
                for child in children:
                    child.parent = None
                    child.save(update_fields=['parent_id'])

        # The criteria_playlist will be deleted automatically via CASCADE
        return self._handle_destroy()

    @extend_schema(parameters=[OpenApiParameter(name=FilterFields.NAME_PUBLIC,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=FilterFields.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY,
                                                required=False)],
                   responses=CriteriaSimpleSerializer)
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs) -> Response:
        return self._handle_retrieve()

    @transaction.atomic
    @extend_schema(request=CriteriaPutSerializer,
                   responses=CriteriaDetailedSerializer,
                   description="""Updates a criteria""")
    def update(self, request, *args, **kwargs):
        return self._handle_update(request)
