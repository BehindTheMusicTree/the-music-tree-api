

from bodzify_api import settings
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.field.TreeField import TreeField


class CriteriaTreeImportSerializer(AppSerializer):
    tree: TreeField = TreeField(allow_empty=False, max_nodes_count=settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT)
