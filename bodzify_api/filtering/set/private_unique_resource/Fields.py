
from bodzify_api.model.private_unique_resource.Fields import     Fields as ModelFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    CREATED_ON_GT = ModelFields.CREATED_ON + '_gt'
    CREATED_ON_LT = ModelFields.CREATED_ON + '_lt'
    CREATED_ON_GTE = ModelFields.CREATED_ON + '_gte'
    CREATED_ON_LTE = ModelFields.CREATED_ON + '_lte'
    UPDATED_ON = ModelFields.UPDATED_ON
    UPDATED_ON_GT = ModelFields.UPDATED_ON + '_gt'
    UPDATED_ON_LT = ModelFields.UPDATED_ON + '_lt'
    UPDATED_ON_GTE = ModelFields.UPDATED_ON + '_gte'
    UPDATED_ON_LTE = ModelFields.UPDATED_ON + '_lte'
