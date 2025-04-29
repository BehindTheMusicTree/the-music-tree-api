from enum import Enum


class CriteriaTypePks(Enum):
    GENRE = 0
    TAG = 1

    def __int__(self):
        return self.value
