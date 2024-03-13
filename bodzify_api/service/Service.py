#!/usr/bin/env python

from abc import abstractmethod
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
        put_schema_serializer = self._get_put_schema_serializer(
            old_instance=old_instance, put_schema_data=put_schema_data)
        put_schema_serializer.is_valid(raise_exception=True)

        return self._save(user=user, save_schema_data=put_schema_data, old_instance=old_instance)

    def _save(self, user: User, save_schema_data: QueryDict, old_instance):
        save_model_data = self._get_save_model_data_from_save_schema_data(
            user=user, save_schema_data=save_schema_data, old_instance=old_instance)
        save_serializer = self._get_save_model_serializer(
            old_instance=old_instance,
            save_model_data=save_model_data,
            partial=True)
        save_serializer.is_valid(raise_exception=True)
        return save_serializer.save()

    def _get_save_model_data_from_save_schema_data(
            self, user: User, save_schema_data: QueryDict, old_instance=None) -> QueryDict:
        save_model_data = save_schema_data.copy()
        save_model_data['user'] = user.pk
        return save_model_data

    def _get_save_schema_data_from_put_schema_data(
            self, user: User, put_schema_data: QueryDict, old_instance=None) -> QueryDict:
        return put_schema_data

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

    @staticmethod
    def _update_data1_with_key_if_set_in_data2(
            key: str, data1: QueryDict, data2: QueryDict) -> QueryDict:
        if key in data2:
            value = data2[key]
            if value == "":
                value = None
            data1[key] = value
        return data1

    @staticmethod
    def _remove_none_or_empty_key_from_dict(dict):
        for key in list(dict.keys()):
            if dict[key] is None or dict[key] == "":
                del dict[key]
        return dict

    @staticmethod
    def _get_dict1_overriden_with_dict2_for_each_key_provided_in_dict2(
            dict1: QueryDict, dict2: QueryDict, keys: list[str]) -> QueryDict:
        overriden_dict1 = dict1.copy()
        for key in keys:
            overriden_dict1 = Service._update_data1_with_key_if_set_in_data2(
                key=key,
                data1=overriden_dict1,
                data2=dict2)
        return overriden_dict1
