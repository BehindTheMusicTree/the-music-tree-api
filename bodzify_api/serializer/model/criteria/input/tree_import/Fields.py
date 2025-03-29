from ..Fields import Fields as InputFields


class Fields:
    TREE_INTERNAL: str = InputFields.TREE_INTERNAL
    TREE_PUBLIC: str = f"{InputFields.TREE_INTERNAL}[]"
    NAME_PUBLIC: str = InputFields.NAME_PUBLIC
    CHILDREN: str = InputFields.CHILDREN
