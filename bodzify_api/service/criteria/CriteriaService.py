
from bodzify_api.model.user.User import User
from rest_framework.request import Request

from bodzify_api.model.criteria.Criteria import Fields as ModelFields
from bodzify_api.serializer.schema.criteria.input.model import CriteriaModelSerializer
from bodzify_api.serializer.schema.criteria.input.endpoint.post import CriteriaPostSerializer
from bodzify_api.serializer.schema.criteria.input.endpoint.put import CriteriaPutSerializer
from bodzify_api.serializer.schema.criteria.input.schema.schema import CriteriaSchemaSerializer
from bodzify_api.service.Service import Service


class CriteriaService(Service):

    def __init__(self, criteria_type_id) -> None:
        self.criteria_type_id = criteria_type_id
        super().__init__()

    def _get_schema_serializer(self, oldinstance, schema_data: dict, request: Request):
        return CriteriaSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request):
        return CriteriaModelSerializer(instance=oldinstance,
                                       data=model_data,
                                       partial=partial,
                                       context={'request': request},)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        schema_data = post_data.copy()

        parent_key = ModelFields.PARENT
        if parent_key in post_data:
            parent_uuid = post_data[parent_key]
            if parent_uuid is None:
                parent_uuid = ""
        else:
            parent_uuid = ""
        schema_data[ModelFields.PARENT] = parent_uuid
        return schema_data

    def _get_schema_data_from_put_data(self, put_data: dict, oldinstance) -> dict:
        return put_data

    def _get_model_data_from_schema_data_not_including_user_field(
            self, user: User, schema_data: dict, oldinstance) -> dict:
        model_data = dict()

        self._update_data1_with_key_if_set_in_data2(key=ModelFields.NAME,
                                                    data1=model_data,
                                                    data2=schema_data)

        self._update_data1_with_key_if_set_in_data2(key=ModelFields.PARENT,
                                                    data1=model_data,
                                                    data2=schema_data)

        model_data[ModelFields.TYPE] = self.criteria_type_id

        return model_data
