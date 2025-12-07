from enum import Enum

from api.model.criteria.Fields import Fields as CriteriaFields


class CriteriaFieldInputType(Enum):
    UUID = CriteriaFields.UUID
    NAME = CriteriaFields.NAME_PUBLIC
