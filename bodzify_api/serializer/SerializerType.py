from enum import Enum


class SerializerType(str, Enum):
    SIMPLE = "simple"
    DETAILED = "detailed"
    CREATE = "create"
    UPDATE = "update"

    @property
    def class_name(self) -> str:
        return f"{self.value}_serializer_class"
