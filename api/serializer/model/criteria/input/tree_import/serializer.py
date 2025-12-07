

from api import settings
from api.serializer.AppInputSerializer import AppInputSerializer
from api.serializer.field.TreeField import TreeField


class CriteriaTreeImportSerializer(AppInputSerializer):
    tree: TreeField = TreeField(allow_empty=False, max_nodes_count=settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT)
