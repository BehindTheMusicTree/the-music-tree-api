from ..Fields import Fields as InputFields


class Fields:
    TREE_INTERNAL: str = InputFields.TREE_INTERNAL
    DATA_PUBLIC: str = f"{TREE_INTERNAL}[]"
    NAME_PUBLIC: str = InputFields.NAME_PUBLIC
    CHILDREN: str = InputFields.CHILDREN
