#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.criteria.input.schema.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.input.CriteriaSaveModelSerializer import CriteriaSaveModelSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaUpdateSchemaSerializer import CriteriaUpdateSchemaSerializer


class CriteriaService:

    def create(self, user: User, create_schema_data: QueryDict) -> Criteria:

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

        criteria = self._save(user=user, save_schema_data=create_schema_data, old_criteria=None)

        CriteriaPlaylist(user=user, type_id=CriteriaTypesId.GENRE, criteria=criteria).save()

        return criteria
    
    def update(self, user: User, update_schema_data: QueryDict, old_criteria: Criteria):
        serializer = CriteriaUpdateSchemaSerializer(data=update_schema_data)
        serializer.is_valid(raise_exception=True)
        return self._save(user=user, save_schema_data=update_schema_data, old_criteria=old_criteria)
    
    def _save(self, user: User, save_schema_data: QueryDict, old_criteria: Criteria = None):
        save_model_data = self._get_save_model_data_from_save_schema_data(
            user=user, 
            save_schema_data=save_schema_data, 
            old_criteria=old_criteria)
        save_model_data[CRITERIA_ATTRIBUTES_LABEL.USER] = user.id

        save_serializer = CriteriaSaveModelSerializer(instance=old_criteria, data=save_model_data, partial=True)
        save_serializer.is_valid(raise_exception=True)
        saved_criteria = save_serializer.save()

        self._update_root_of_descandants_if_needed(old_criteria, saved_criteria)

        return saved_criteria
    
    def _update_root_of_criteria_and_children(self, criteria: Criteria, new_root: Criteria):
        criteria.root = new_root
        children = criteria.get_children()
        if children.exists():
            for child in children:
                self._update_root_of_criteria_and_children(child, new_root)
    
    def _update_root_of_descandants_if_needed(self, old_criteria: Criteria, saved_criteria: Criteria):
        if old_criteria is not None and old_criteria.root != saved_criteria.root:
            self._update_root_of_criteria_and_children(saved_criteria, saved_criteria.root)
    
    def _get_save_model_data_from_save_schema_data(self, 
            user: User, save_schema_data: QueryDict, old_criteria: Criteria = None) -> dict:
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

        save_model_data = self._get_save_model_data_updated_with_root_if_needed(
            save_model_data=save_model_data, 
            old_criteria=old_criteria)

        return save_model_data
    
    def _get_save_model_data_updated_with_root_if_needed(self, save_model_data: dict, old_criteria: Criteria):
        parent_key = CRITERIA_ATTRIBUTES_LABEL.PARENT
        is_parent_updated = False
        if parent_key in save_model_data:
            parent_uuid = save_model_data[parent_key]
            if old_criteria is None or old_criteria.parent is None:
                is_parent_updated = True
            elif parent_uuid != old_criteria.parent.uuid:
                is_parent_updated = True

        if is_parent_updated:
            if parent_uuid in ["", None]: 
                root_uuid = None
            else:
                root_uuid = Criteria.objects.get(uuid=parent_uuid).root.uuid
            save_model_data[CRITERIA_ATTRIBUTES_LABEL.ROOT] = root_uuid
        return save_model_data
    
    def _get_query_dict_updated_with_dict_key_if_set(self, key: str, dict: dict, query_dict: QueryDict):
        if key in query_dict:
            value = query_dict[key]
            if value == "":
                value = None
            dict[key] = value
        return dict
    
    def get_criteria_playlist_class(self):
        raise NotImplementedError("You should implement this method in a subclass")


    def getCriteriaFromNameAfterHavingEventuallyCreatedIt(
        self, user: User, criteriaName: str) -> Criteria:

        if Criteria.objects.filter(user=user, type_id=self.get_criteria_type_id(), name=criteriaName).exists():
            criteria = Criteria.objects.get(user=user, type_id=self.get_criteria_type_id(), name=criteriaName)
        else:
            criteria = Criteria.objects.create(
                user=user, type_id=self.get_criteria_type_id(), name=criteriaName)
            CriteriaPlaylist(user=user, type_id=CriteriaTypesId.GENRE, criteria=criteria).save()    
        return criteria

    def get_criteria_type_id(self):
        raise NotImplementedError("You should implement this method in a subclass")