#!/usr/bin/env python

from abc import abstractmethod
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer


class Service:

    @abstractmethod
    def _get_post_serializer(self, post_data: dict) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_put_serializer(self, old_instance, put_data: dict) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_save_schema_serializer(self, old_instance, save_schema_data: dict, request) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_save_schema_data_from_post_data(self, post_data: dict) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_save_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_save_model_data_from_save_schema_data_not_including_user_field(self,
                                                                            user: User,
                                                                            save_schema_data: dict,
                                                                            old_instance=None) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @staticmethod
    def _update_data1_with_key_if_set_in_data2(key: str, data1: dict, data2: dict) -> dict:
        if key in data2:
            value = data2[key]
            if value == "":
                value = None
            data1[key] = value
        return data1

    @staticmethod
    def _update_data1_converting_str_to_int_value_if_set(key: str, data1: dict):
        if key in data1:
            if data1[key] is not None and data1[key] != '':
                rating = int(data1[key])
            else:
                rating = None
            data1[key] = rating

    @staticmethod
    def _remove_none_or_empty_key_from_dict(dict):
        for key in list(dict.keys()):
            if dict[key] is None or dict[key] == "":
                del dict[key]
        return dict

    @staticmethod
    def _override_data1_with_data2_values_for_each_key_in_data2(data1: dict, data2: dict, keys: list[str]):
        for key in keys:
            Service._update_data1_with_key_if_set_in_data2(key=key, data1=data1, data2=data2)
        return data1

    @staticmethod
    def _get_copy_of_dict_including_only_specified_keys(dict, keys):
        dict2 = dict.copy()
        for key in list(dict2.keys()):
            if key not in keys:
                del dict2[key]
        return dict2

    def create(self, post_data: dict, request):
        post_serializer = self._get_post_serializer(post_data=post_data)
        post_serializer.is_valid(raise_exception=True)
        save_schema_data = self._get_save_schema_data_from_post_data(post_data=post_data)
        return self._save(save_schema_data=save_schema_data, old_instance=None, request=request)

    def update(self, put_data: dict, old_instance, request):
        put_serializer = self._get_put_serializer(old_instance=old_instance,
                                                  put_data=put_data)
        put_serializer.is_valid(raise_exception=True)
        save_schema_data = self._get_save_schema_data_from_put_data(put_data=put_data,
                                                                    old_instance=old_instance)
        return self._save(save_schema_data=save_schema_data, old_instance=old_instance, request=request)

    def _save(self, save_schema_data: dict, old_instance, request):
        save_schema_serializer = self._get_save_schema_serializer(old_instance=old_instance,
                                                                  save_schema_data=save_schema_data,
                                                                  request=request)
        save_schema_serializer.is_valid(raise_exception=True)

        save_model_data = self._get_save_model_data_from_save_schema_data_not_including_user_field(
            user=request.user, save_schema_data=save_schema_data, old_instance=old_instance)
        save_model_data['user'] = request.user.pk
        save_model_serializer = self._get_save_model_serializer(
            old_instance=old_instance,
            save_model_data=save_model_data,
            partial=True)
        save_model_serializer.is_valid(raise_exception=True)
        return save_model_serializer.save()
