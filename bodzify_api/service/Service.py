#!/usr/bin/env python

from abc import abstractmethod
from typing import Optional
from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework.serializers import Serializer


class Service:
    
    def create(self, user: User, post_schema_data: QueryDict):
        post_schema_serializer = self._get_post_schema_serializer(post_schema_data=post_schema_data)
        post_schema_serializer.is_valid(raise_exception=True)
        post_schema_data = self._get_save_schema_data_from_post_schema_data(post_schema_data=post_schema_data)
        return self._save(user=user, save_schema_data=post_schema_data, old_instance=None)
    
    def update(self, user: User, put_schema_data: QueryDict, old_instance):
        put_schema_serializer = self._get_put_schema_serializer(old_instance=old_instance, put_schema_data=put_schema_data)
        put_schema_serializer.is_valid(raise_exception=True)
        return self._save(user=user, save_schema_data=put_schema_data, old_instance=old_instance)
    
    def _save(self, user: User, save_schema_data: QueryDict, old_instance):
        save_model_data = self._get_save_model_data_from_save_schema_data(user=user, save_schema_data=save_schema_data)        
        save_serializer = self._get_save_model_serializer(
            old_instance=old_instance, 
            save_model_data=save_model_data, 
            partial=True)
        save_serializer.is_valid(raise_exception=True)
        return save_serializer.save()
    
    @abstractmethod
    def _get_post_schema_serializer(self, post_schema_data: QueryDict) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")
    
    @abstractmethod
    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")
    
    @abstractmethod
    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")
    
    @abstractmethod
    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        raise NotImplementedError("You should implement this method in a subclass")
    
    @abstractmethod
    def _get_save_model_data_from_save_schema_data(self, 
                                                   user: Optional[User],
                                                   save_schema_data: QueryDict) -> QueryDict:
        raise NotImplementedError("You should implement this method in a subclass")
    
    @staticmethod
    def get_querydict1_updated_with_querydict2_key_if_set(key: str, querydict1: QueryDict, querydict2: QueryDict) -> QueryDict:
        if key in querydict2:
            value = querydict2[key]
            if value == "":
                value = None
            querydict1[key] = value
        return querydict1