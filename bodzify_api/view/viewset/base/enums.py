from enum import Enum


class SerializerType(str, Enum):
    SIMPLE = "simple"
    DETAILED = "detailed"
    CREATE = "create"
    UPDATE = "update"

    @property
    def class_name(self) -> str:
        return f"{self.value}_serializer_class"


class PaginatedResponseFields:
    OVERALL_TOTAL = 'overallTotal'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'


class HttpMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'