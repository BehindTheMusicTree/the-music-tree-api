import re
from typing import Any, Generic, Sequence, Type, TypeVar, Union, cast

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from bodzify_api.filtering.backend.ConsistentParametersFilterBackend import ConsistentParametersFilterBackend
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer, ModelSerializer, Serializer

from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.model.private.Fields import Fields as PrivateFields
from bodzify_api.serializer.SerializerType import SerializerType
from bodzify_api.view.file_response.AppFileResponse import AppFileResponse
from ...pagination.AppPagination import AppPagination
# UUID format: 8-4-4-4-12 hexadecimal digits
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')


T = TypeVar('T', bound=BaseModel)


class AppModelViewSet(viewsets.ModelViewSet, Generic[T]):
    pagination_class = AppPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [ConsistentParametersFilterBackend]
    model_class: Type[T]
    filterset_class: Type[AppFilterSet] = AppFilterSet
    simple_serializer_class: Type[ModelSerializer] | None = None
    detailed_serializer_class: Type[ModelSerializer] | None = None
    create_serializer_class: Type[Serializer] | None = None
    update_serializer_class: Type[Serializer] | None = None
    is_private_resource: bool = True
    is_pk_uuid: bool = True

    def __init__(self, model_class: Type[T],
                 filterset_class: Type[AppFilterSet] = AppFilterSet,
                 simple_serializer_class: Type[ModelSerializer] | None = None,
                 detailed_serializer_class: Type[ModelSerializer] | None = None,
                 update_serializer_class: Type[Serializer] | None = None,
                 create_serializer_class: Type[Serializer] | None = None,
                 is_private_resource: bool = True,
                 is_pk_uuid: bool = True,
                 **kwargs):
        super().__init__(**kwargs)
        self.model_class = model_class
        self.filterset_class = filterset_class
        self.simple_serializer_class = simple_serializer_class
        self.detailed_serializer_class = detailed_serializer_class
        self.update_serializer_class = update_serializer_class
        self.create_serializer_class = create_serializer_class
        self.is_private_resource = is_private_resource
        self.is_pk_uuid = is_pk_uuid

    def _require_serializer(self, serializer_type: SerializerType) -> Type[Union[ModelSerializer, Serializer]]:
        serializer = getattr(self, serializer_type.class_name, None)
        if not serializer:
            raise ImproperlyConfigured(f"Serializer {serializer_type.class_name} not defined in viewset")
        return serializer

    def _get_validated_data(self, serializer: Union[Serializer, ModelSerializer, BaseSerializer]) -> dict[str, Any]:
        serializer.is_valid(raise_exception=True)
        validated_data_dict = getattr(serializer, 'validated_data', {})
        if PrivateFields.USER not in validated_data_dict:
            validated_data_dict[PrivateFields.USER] = self.request.user
        return validated_data_dict

    def _inject_user(self, data: dict[str, Any], request: Request) -> dict[str, Any]:
        if PrivateFields.USER not in data:
            data[PrivateFields.USER] = request.user
        return data

    def _create_instance(self, request: Request, create_data: dict[str, Any]) -> T:
        serializer_class = self._require_serializer(SerializerType.CREATE)
        serializer = serializer_class(data=create_data, context={'request': request})
        validated_data = self._get_validated_data(serializer)

        return self.model_class.objects.create(**validated_data)

    def _update_instance(self, request: Request, instance: T, update_data: dict[str, Any]) -> T:
        serializer_class = self._require_serializer(SerializerType.UPDATE)
        serializer = serializer_class(instance=instance, data=update_data, partial=True, context={'request': request})
        validated_data = self._get_validated_data(serializer)
        return self.model_class.objects.update_instance(instance, **validated_data)

    def _get_paginated_list_response(self, queryset, serializer_type=SerializerType.SIMPLE,
                                     status_code=status.HTTP_200_OK) -> Response:
        """
        Get a paginated response for a list view.

        Args:
            queryset: The queryset to paginate
            serializer_type: The type of serializer to use (defaults to SIMPLE)
            status_code: The HTTP status code to return (defaults to 200 OK)

        Returns:
            Response with pagination metadata and the specified status code
        """
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self._require_serializer(serializer_type)(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.status_code = status_code
            return response

        # If pagination is disabled
        serializer = self._require_serializer(serializer_type)(queryset, many=True)
        return Response(serializer.data, status=status_code)

    def _handle_list(self) -> Response:
        queryset = self.get_queryset()
        return self._get_paginated_list_response(queryset)

    def _get_post_created_response(self, serializer: Serializer) -> Response:
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _handle_post(self, request: Request) -> Response:
        instance = self._create_instance(request=request, create_data=request.data)
        serializer = self._require_serializer(SerializerType.DETAILED)(instance=instance)
        return self._get_post_created_response(serializer)

    def _handle_retrieve(self) -> Response:
        serializer = self._require_serializer(SerializerType.DETAILED)(self.get_object())
        return Response(serializer.data)

    def _handle_update(self, request: Request) -> Response:
        updated_instance = self._update_instance(request=request, instance=self.get_object(), update_data=request.data)
        serializer = self._require_serializer(SerializerType.DETAILED)(instance=updated_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def _handle_destroy(self) -> Response:
        self.model_class.objects.delete_instance(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    def paginate_queryset(self, queryset) -> Union[list[T], QuerySet[T]] | None:
        if self.paginator is None:
            return None
        if isinstance(queryset, Sequence) and not isinstance(queryset, QuerySet):
            queryset = self.model_class.objects.filter(id__in=[obj.id for obj in queryset])
        return self.paginator.paginate_queryset(cast(QuerySet[T], queryset), self.request, view=self)

    def get_object(self) -> T:
        from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
        from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

        # Use a direct query instead of relying on the DRF lookup mechanism
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        # Validate eventually UUID format if the field is 'pk'
        if self.lookup_field == 'pk' and self.is_pk_uuid and not UUID_PATTERN.match(lookup_value):
            raise AppValidationException(
                message=f"Invalid UUID format: {lookup_value}",
                field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID,
                field_name=self.lookup_field
            )

        try:
            if self.is_private_resource:
                filter_kwargs = {
                    self.lookup_field: lookup_value,
                    'user': self.request.user
                }
            else:
                filter_kwargs = {
                    self.lookup_field: lookup_value,
                }

            obj = self.model_class.objects.get(**filter_kwargs)
            return obj
        except self.model_class.DoesNotExist:
            # Fall back to the standard DRF lookup if direct lookup fails
            return super().get_object()

    def get_serializer_class_for_non_standard_action(self) -> Type[Serializer]:
        raise NotImplementedError(f"Action {self.action} not defined in viewset")

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            return self._require_serializer(SerializerType.DETAILED)
        elif self.action == 'create':
            return self._require_serializer(SerializerType.CREATE)
        elif self.action in ['update', 'partial_update']:
            return self._require_serializer(SerializerType.UPDATE)
        else:
            return self.get_serializer_class_for_non_standard_action()

    def get_queryset(self):
        request: Request = cast(Request, self.request)
        if self.is_private_resource:
            queryset = self.model_class.objects.filter(user=request.user)
        else:
            queryset = self.model_class.objects.all()

        ordering_fields = cast(BaseModel, self.model_class).objects.get_default_ordering()
        return queryset.order_by(*ordering_fields)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    def get_file_response(self, file_path: str):
        return AppFileResponse.from_file(file_path=file_path, filename=file_path.split('/')[-1])

    def retrieve(self, *args, **kwargs) -> Response:
        raise MethodNotAllowed('GET', detail='Retrieve operation not allowed for this resource')

    def create(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('POST', detail='Create operation not allowed for this resource')

    def list(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('GET', detail='list operation not allowed for this resource')

    def update(self, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('PUT', detail='Update operation not allowed for this resource')

    def destroy(self, *args, **kwargs) -> Response:
        raise MethodNotAllowed('DELETE', detail='Delete operation not allowed for this resource')
