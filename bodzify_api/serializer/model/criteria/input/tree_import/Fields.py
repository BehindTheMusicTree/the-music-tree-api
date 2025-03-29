from ..Fields import Fields as InputFields


class Fields:
    DATA_INTERNAL: str = InputFields.DATA_INTERNAL
    DATA_PUBLIC: str = f"{DATA_INTERNAL}[]"
    NAME_PUBLIC: str = InputFields.NAME_PUBLIC
    CHILDREN: str = InputFields.CHILDREN
