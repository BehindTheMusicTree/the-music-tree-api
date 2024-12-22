
from typing import Dict, Generic, Sequence, Type, Optional, TypeVar, Any, List, Union, cast
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer, BaseSerializer
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError as DrfValidationError, MethodNotAllowed
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import FileResponse
from django.db.models import QuerySet

from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.model.private.Fields import Fields as PrivateFields
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.serializer.SerializerType import SerializerType
from bodzify_api.utils import data_transformer
from bodzify_api.view.error.ErrorCode import ErrorCode
from bodzify_api.view.error.ErrorMessages import AppErrorMessages
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.file_response.AppFileResponse import AppFileResponse
from bodzify_api.view.HttpMethod import HttpMethod
from ....pagination.AppPagination import AppPagination


T = TypeVar('T', bound=BaseModel)


class AppModelViewSet(viewsets.ModelViewSet, Generic[T]):
    pagination_class = AppPagination
    permission_classes = [IsAuthenticated]
    model_class: Type[T]
    filter_class: Type[AppFilterSet] = AppFilterSet
    simple_serializer_class: Optional[Type[ModelSerializer]] = None
    detailed_serializer_class: Optional[Type[ModelSerializer]] = None
    create_serializer_class: Optional[Type[Serializer]] = None
    update_serializer_class: Optional[Type[Serializer]] = None

    def __init__(self,
                 model_class: Type[T],
                 filterset_class: Type[AppFilterSet] = AppFilterSet,
                 simple_serializer_class: Optional[Type[ModelSerializer]] = None,
                 detailed_serializer_class: Optional[Type[ModelSerializer]] = None,
                 update_serializer_class: Optional[Type[Serializer]] = None,
                 create_serializer_class: Optional[Type[Serializer]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.model_class = model_class
        self.filter_class = filterset_class
        self.simple_serializer_class = simple_serializer_class
        self.detailed_serializer_class = detailed_serializer_class
        self.update_serializer_class = update_serializer_class
        self.create_serializer_class = create_serializer_class

    def _require_serializer(self, serializer_type: SerializerType) -> Type[Union[ModelSerializer, Serializer]]:
        serializer = getattr(self, serializer_type.class_name, None)
        if not serializer:
            raise DrfValidationError(
                detail={
                    'message': AppErrorMessages.MESSAGES[ErrorCode.SYSTEM_SERIALIZER_NOT_DEFINED],
                    'code': 'serializer_not_defined'
                }
            )
        return serializer

    def _get_create_serializer_class(self) -> Type[Serializer]:
        if self.create_serializer_class:
            return self.create_serializer_class
        raise DrfValidationError(
            detail={
                'message': AppErrorMessages.MESSAGES[ErrorCode.SYSTEM_SERIALIZER_NOT_DEFINED],
                'code': 'serializer_not_defined'
            }
        )

    def _get_validated_data(self, serializer: Union[Serializer, ModelSerializer, BaseSerializer]) -> Dict[str, Any]:
        serializer.is_valid(raise_exception=True)
        validated_data_dict = getattr(serializer, 'validated_data', {})
        if not validated_data_dict:
            raise DrfValidationError(
                detail={
                    'message': "Serializer validation failed - no validated data available",
                    'code': "validation_error"
                }
            )
        validated_data_dict = {str(k): v for k, v in validated_data_dict.items()}
        if PrivateFields.USER not in validated_data_dict:
            validated_data_dict[PrivateFields.USER] = self.request.user
        return validated_data_dict

    def _inject_user(self, data: Dict[str, Any], request: Request) -> Dict[str, Any]:
        if PrivateFields.USER not in data:
            data[PrivateFields.USER] = request.user
        return data

    def _create_instance(
            self, request: Request, create_data: Dict[str, Any], creation_type: Optional[str]) -> T:
        if self.action != 'create':
            raise NotImplementedError(f"No action defined for action {self.action}")

        serializer_class = self._get_create_serializer_class()
        serializer = serializer_class(data=create_data, context={'request': request})
        validated_data = self._get_validated_data(serializer)
        if creation_type:
            instance = self.model_class.objects.create(creation_type=creation_type, **validated_data)
        else:
            instance = self.model_class.objects.create(**validated_data)
        instance.save()
        return instance

    def _update_instance(self, request: Request, instance: T, update_data: Dict[str, Any]) -> T:
        serializer_class = self._require_serializer(SerializerType.UPDATE)
        serializer = serializer_class(data=update_data, partial=True, context={'request': request})
        validated_data = self._get_validated_data(serializer)
        return self.model_class.objects.update_instance(instance, **validated_data)

    def _handle_list(self) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if not queryset.exists():
            data = []
        elif page is not None:
            serializer = self._require_serializer(SerializerType.SIMPLE)(page, many=True)
            data = list(serializer.data)
        else:
            data = []

        return self.get_paginated_response(data)

    def _handle_post(self, request: Request, creation_type: Optional[str] = None) -> Response:
        create_data_in_snake_case = data_transformer.dict_to_snake_case(request.data)
        instance = self._create_instance(request=request,
                                         create_data=create_data_in_snake_case,
                                         creation_type=creation_type)
        serializer = self._require_serializer(SerializerType.DETAILED)(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _handle_retrieve(self) -> Response:
        instance = self.get_object()
        serializer = self._require_serializer(SerializerType.DETAILED)(instance)
        return Response(serializer.data)

    def _handle_update(self, request: Request) -> Response:
        instance = self.get_object()
        update_data_in_camel_case = data_transformer.convert_data_to_dict(request.data)
        update_data_in_snake_case = data_transformer.dict_to_snake_case(update_data_in_camel_case)
        updated_instance = self._update_instance(request=request,
                                                 instance=instance,
                                                 update_data=update_data_in_snake_case)
        serializer = self._require_serializer(SerializerType.DETAILED)(instance=updated_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _handle_destroy(self) -> Response:
        instance = self.get_object()
        self.model_class.objects.delete_instance(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def paginate_queryset(self, queryset) -> Optional[Union[List[T], QuerySet[T]]]:
        if self.paginator is None:
            return None
        if isinstance(queryset, Sequence) and not isinstance(queryset, QuerySet):
            queryset = self.model_class.objects.filter(id__in=[obj.id for obj in queryset])
        return self.paginator.paginate_queryset(cast(QuerySet[T], queryset), self.request, view=self)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, (DrfValidationError, DjangoValidationError)):
            return ErrorResponse.from_validation_error(exc)
        return super().handle_exception(exc)

    def get_object(self) -> T:
        return super().get_object()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            return self._require_serializer(SerializerType.DETAILED)
        elif self.action == 'create':
            return self._get_create_serializer_class()
        elif self.action in ['update', 'partial_update']:
            return self._require_serializer(SerializerType.UPDATE)
        raise NotImplementedError(f"Action {self.action} not defined in viewset")

    def get_queryset(self):
        request: Request = cast(Request, self.request)
        queryset = self.model_class.objects.filter(user=request.user)

        if request.method == HttpMethod.GET:
            query_params_snake_case = data_transformer.dict_to_snake_case(request.query_params)
            queryset = self.filter_class(query_params_snake_case, queryset=queryset).qs

        ordering_fields = cast(BaseModel, self.model_class).objects.get_default_ordering()
        return queryset.order_by(*ordering_fields)

    def get_file_response(self, file_path: str) -> FileResponse:
        return AppFileResponse.from_file(file_path=file_path, filename=file_path.split('/')[-1])

    def retrieve(self, *args, **kwargs) -> Response:
        raise MethodNotAllowed('GET', detail='Retrieve operation not allowed for this resource')

    def create(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('POST', detail='Create operation not allowed for this resource')

    def list(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('GET', detail='List operation not allowed for this resource')

    def update(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('PUT', detail='Update operation not allowed for this resource')

    def destroy(self, *args, **kwargs) -> Response:
        raise MethodNotAllowed('DELETE', detail='Delete operation not allowed for this resource')
