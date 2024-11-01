
from abc import abstractmethod
from rest_framework.request import Request

from bodzify_api.model.user.User import User
from rest_framework.request import Request
from rest_framework.serializers import Serializer

from bodzify_api.model.base.utils.PrivateModel import Fields


class Service:

    @abstractmethod
    def _get_schema_serializer(self, oldinstance, schema_data: dict, request: Request) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request) -> Serializer:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_schema_data_from_put_data(self, put_data: dict, oldinstance=None) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @abstractmethod
    def _get_model_data_from_schema_data_not_including_user_field(self,
                                                                  user: User,
                                                                  schema_data: dict,
                                                                  oldinstance=None) -> dict:
        raise NotImplementedError("You should implement this method in a subclass")

    @staticmethod
    def _update_data1_with_key_if_set_in_data2(key: str, data1: dict, data2: dict):
        if key in data2:
            value = data2[key]
            if value == "":
                value = None
            data1[key] = value

    @staticmethod
    def _update_data1_converting_str_to_int_value_if_set(key: str, data1: dict):
        if key in data1:
            if data1[key] and data1[key] != '':
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

    @staticmethod
    def _get_copy_of_dict_including_only_specified_keys(dict, keys):
        dict2 = dict.copy()
        for key in list(dict2.keys()):
            if key not in keys:
                del dict2[key]
        return dict2

    def _save(self, schema_data: dict, oldinstance, request: Request, partial: bool):
        schema_serializer = self._get_schema_serializer(oldinstance=oldinstance,
                                                        schema_data=schema_data,
                                                        request=request)
        schema_serializer.is_valid(raise_exception=True)

        model_data = self._get_model_data_from_schema_data_not_including_user_field(user=request.user,
                                                                                    schema_data=schema_data,
                                                                                    oldinstance=oldinstance)
        model_data[Fields.USER] = request.user.pk

        model_serializer = self._get_model_serializer(oldinstance=oldinstance,
                                                      model_data=model_data,
                                                      partial=partial,
                                                      request=request,)
        model_serializer.is_valid(raise_exception=True)

        return model_serializer.save()

    def post(self, create_data_validated: dict, request: Request):
        schema_data = self._get_schema_data_from_post_data(post_data=create_data_validated)
        return self._save(schema_data=schema_data, oldinstance=None, request=request, partial=False)

    def update(self, put_data: dict, oldinstance, request: Request):
        schema_data = self._get_schema_data_from_put_data(put_data=put_data, oldinstance=oldinstance)
        return self._save(schema_data=schema_data, oldinstance=oldinstance, request=request, partial=True)
