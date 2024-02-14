#!/usr/bin/env python

from typing import Optional
import logging
from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.criteria.input.schema.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.input.CriteriaSaveModelSerializer import CriteriaSaveModelSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaUpdateSchemaSerializer import CriteriaUpdateSchemaSerializer
from django.db.models import QuerySet

logger = logging.getLogger('bodzify_api')

class CriteriaService:

    def create(self, user: User, create_schema_data: QueryDict):
        schema_serializer = CriteriaPostSchemaSerializer(data=create_schema_data)
        schema_serializer.is_valid(raise_exception=True)

        create_schema_data[CRITERIA_ATTRIBUTES_LABEL.USER] = user.pk

        parent_key = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if parent_key in create_schema_data:
            parent_uuid = create_schema_data[parent_key]
            if parent_uuid in ["", None]:
                parent_uuid = None
        else:
            parent_uuid = None
        create_schema_data[CRITERIA_ATTRIBUTES_LABEL.PARENT] = parent_uuid

        return self._save(user=user, save_schema_data=create_schema_data, old_criteria=None)
    
    def update(self, user: User, update_schema_data: QueryDict, old_criteria: Criteria):
        serializer = CriteriaUpdateSchemaSerializer(instance=old_criteria, data=update_schema_data)
        serializer.is_valid(raise_exception=True)
        return self._save(user=user, save_schema_data=update_schema_data, old_criteria=old_criteria)
    
    def _save(self, user: User, save_schema_data: QueryDict, old_criteria: Optional[Criteria]):
        save_model_data = self._get_save_model_data_from_save_schema_data(save_schema_data=save_schema_data)        
        save_model_data[CRITERIA_ATTRIBUTES_LABEL.USER] = user.pk

        save_serializer = CriteriaSaveModelSerializer(instance=old_criteria, data=save_model_data, partial=True)
        save_serializer.is_valid(raise_exception=True)

        return save_serializer.save()
        
    def _update_playlists_when_updated_criteria_is_root(self, old_parent: Criteria, criteria_playlist_tracks: QuerySet):
        self._remove_tracks_from_playlist_of_criteria_and_ascendants(
            criteria=old_parent, tracks=criteria_playlist_tracks)
    
    def _remove_tracks_from_playlist_of_criteria_and_ascendants(self, criteria: Criteria, tracks: QuerySet):
        CriteriaPlaylist.objects.get(criteria=criteria).tracks.remove(*tracks)
        if criteria.parent is not None:
            self._remove_tracks_from_playlist_of_criteria_and_ascendants(criteria=criteria.parent, tracks=tracks)
        
    def _remove_criteria_playlist_tracks_to_acendants_playlists_of_old_criteria(self, 
                                                                                old_parent: Criteria, 
                                                                                saved_criteria: Criteria):
        tracks = CriteriaPlaylist.objects.get(criteria=saved_criteria).tracks.all()
        self._remove_tracks_from_playlist_of_criteria_and_ascendants(criteria=old_parent, tracks=tracks) 

    def _get_save_model_data_from_save_schema_data(self, save_schema_data: QueryDict) -> dict:
        save_model_data = dict()

        save_model_data = self._get_query_dict_updated_with_dict_key_if_set(
            key=CRITERIA_ATTRIBUTES_LABEL.NAME,
            dict=save_model_data,
            query_dict=save_schema_data)

        save_model_data = self._get_query_dict_updated_with_dict_key_if_set(
            key=CRITERIA_ATTRIBUTES_LABEL.PARENT,
            dict=save_model_data,
            query_dict=save_schema_data)
        
        save_model_data[CRITERIA_ATTRIBUTES_LABEL.TYPE] = self.get_criteria_type_id()

        return save_model_data
    
    def _get_query_dict_updated_with_dict_key_if_set(self, key: str, dict: dict, query_dict: QueryDict):
        if key in query_dict:
            value = query_dict[key]
            if value == "":
                value = None
            dict[key] = value
        return dict

    def get_criteria_from_name_after_having_eventually_created_it(
        self, user: User, criteria_name: str) -> Criteria:

        if Criteria.objects.filter(user=user, type_id=self.get_criteria_type_id(), name=criteria_name).exists():
            criteria = Criteria.objects.get(user=user, type_id=self.get_criteria_type_id(), name=criteria_name)
        else:
            criteria = Criteria.objects.create(user=user, type_id=self.get_criteria_type_id(), name=criteria_name)
        return criteria
    
    def get_criteria_playlist_class(self):
        raise NotImplementedError("You should implement this method in a subclass")

    def get_criteria_type_id(self):
        raise NotImplementedError("You should implement this method in a subclass")