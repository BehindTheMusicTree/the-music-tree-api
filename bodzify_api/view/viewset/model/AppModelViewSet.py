from typing import Dict, Generic, Type, Optional, TypeVar, Any, List, Union, cast

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError, APIException
from rest_framework import viewsets, status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError, MethodNotAllowed
from django.http import FileResponse

from bodzify_api.model.base.utils.base_model.BaseModel import BaseModel
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.service.Service import Service
from bodzify_api.view.errors import APIErrorResponse, APIErrorMessages, APIFileResponse
from bodzify_api.view.viewset.base.RequestHandler import RequestHandler
from bodzify_api.view.viewset.base.ErrorProcessor import ErrorProcessor
from bodzify_api.view.viewset.base.DataTransformer import DataTransformer
from .enums import SerializerType, HttpMethod, PaginatedResponseFields


T = TypeVar('T', bound=BaseModel)


class AppModelViewSet(viewsets.ModelViewSet, Generic[T]):
    permission_classes = [IsAuthenticated]
    model_class: Type[T]
    filter_class: Optional[Type[AppFilterSet]] = None
    simple_serializer_class: Optional[Type[ModelSerializer]] = None
    detailed_serializer_class: Optional[Type[ModelSerializer]] = None
    create_serializer_class: Optional[Type[Serializer]] = None
    update_serializer_class: Optional[Type[Serializer]] = None

    def __init__(
            self,
            model_class: Type[T],
            service: Optional[Service] = None,
            filter_class: Optional[Type[AppFilterSet]] = None,
            simple_serializer_class: Optional[Type[ModelSerializer]] = None,
            detailed_serializer_class: Optional[Type[ModelSerializer]] = None,
            update_serializer_class: Optional[Type[Serializer]] = None,
            create_serializer_class: Optional[Type[Serializer]] = None,
            **kwargs):
        super().__init__(**kwargs)
        self.model_class = model_class
        self.service = service
        self.filter_class = filter_class
        self.simple_serializer_class = simple_serializer_class
        self.detailed_serializer_class = detailed_serializer_class
        self.update_serializer_class = update_serializer_class
        self.create_serializer_class = create_serializer_class
        self.request_handler = RequestHandler()
        self.error_processor = ErrorProcessor()
        self.data_transformer = DataTransformer()

    def _require_serializer(self, serializer_type: SerializerType) -> Type[Union[ModelSerializer, Serializer]]:
        serializer = getattr(self, serializer_type.class_name, None)
        if not serializer:
            raise NotImplementedError(APIErrorMessages.SERIALIZER_NOT_DEFINED[serializer_type])
        return serializer

    def _get_create_serializer(self) -> Type[Serializer]:
        if self.create_serializer_class:
            return self.create_serializer_class
        raise NotImplementedError(APIErrorMessages.SERIALIZER_NOT_DEFINED[SerializerType.CREATE])

    def _require_service(self) -> None:
        if not self.service:
            raise NotImplementedError(APIErrorMessages.SERVICE_NOT_DEFINED)

    def _create_instance(self, request: Request, create_data: Dict[str, Any]) -> T:
        if self.action == 'create':
            self._require_service()
            if self.service is None:  # This will never happen due to _require_service, but needed for type checking
                raise NotImplementedError(APIErrorMessages.SERVICE_NOT_DEFINED)
            return self.service.post(request=request, data_validated=create_data)
        raise NotImplementedError(f"No action defined for action {self.action}")

    def _handle_post(self, request: Request, *args, **kwargs) -> Response:
        self._require_service()
        create_data = self.data_transformer.form_data_to_snake_case(request.data)
        serializer_class = self.get_serializer_class()

        def perform_post() -> Response:
            instance = self._create_instance(request, create_data)
            serializer = self._require_serializer(SerializerType.DETAILED)(instance=instance)
            headers = self.get_success_headers(serializer.data)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        return self.request_handler.handle_validated_request(
            create_data, perform_post, serializer_class, request)

    def _handle_update(self, request: Request, *args, **kwargs) -> Response:
        self._require_service()
        update_data = self.data_transformer.form_data_to_snake_case(request.data)
        serializer_class = self.get_serializer_class()

        def perform_update() -> Response:
            instance = self.get_object()
            if self.service is None:  # This will never happen due to _require_service, but needed for type checking
                raise NotImplementedError(APIErrorMessages.SERVICE_NOT_DEFINED)
            self.service.update(
                data_validated=update_data,
                oldinstance=instance,
                request=request
            )
            serializer = self._require_serializer(SerializerType.DETAILED)(instance=instance)
            headers = self.get_success_headers(serializer.data)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                headers=headers
            )

        return self.request_handler.handle_validated_request(
            update_data, perform_update, serializer_class, request)

    def _handle_list(self, request: Request, *args, **kwargs) -> Response:
        try:
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
        except (DRFValidationError, ValidationError) as e:
            return APIErrorResponse.from_validation_error(e)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, (DRFValidationError, DjangoValidationError)):
            return APIErrorResponse.from_validation_error(exc)
        return super().handle_exception(exc)

    def get_object(self) -> T:
        return super().get_object()

    def get_queryset(self):
        request: Request = cast(Request, self.request)

        queryset = self.model_class.objects.filter(user=request.user)

        if request.method == HttpMethod.GET and self.filter_class:
            try:
                snake_case_params = self.data_transformer.dict_to_snake_case(request.query_params)
                queryset = self.filter_class(snake_case_params, queryset=queryset).qs
            except DjangoValidationError:
                raise ValidationError(detail=APIErrorMessages.INVALID_QUERY_PARAMS)

        ordering_fields = cast(BaseModel, self.model_class).objects.get_default_ordering()
        return queryset.order_by(*ordering_fields)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            return self._require_serializer(SerializerType.DETAILED)
        elif self.action == 'create':
            return self._get_create_serializer()
        elif self.action in ['update', 'partial_update']:
            return self._require_serializer(SerializerType.UPDATE)
        raise NotImplementedError(f"Action {self.action} not defined in viewset")

    def get_paginated_response(self, data: List[Any]) -> Response:
        if not self.paginator:
            raise APIException(
                APIErrorMessages.PAGINATION_NOT_SET,
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            PaginatedResponseFields.OVERALL_TOTAL: self.paginator.page.paginator.count if data else 0,
            PaginatedResponseFields.NEXT: self.paginator.get_next_link() if data else None,
            PaginatedResponseFields.PREVIOUS: self.paginator.get_previous_link() if data else None,
            PaginatedResponseFields.RESULTS: data
        })

    def get_file_response(self, file_path: str) -> FileResponse:
        return APIFileResponse.from_file(file_path=file_path, filename=file_path.split('/')[-1])

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self._require_serializer(SerializerType.DETAILED)(instance)
        return Response(serializer.data)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        raise MethodNotAllowed('DELETE', detail='Delete operation not allowed for this resource')
