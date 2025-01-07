
from bodzify_api.model.private_unique_resource.Fields import Fields as ModelFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    CREATED_ON_GT = ModelFields.CREATED_ON + '_Gt'
    CREATED_ON_LT = ModelFields.CREATED_ON + '_Lt'
    CREATED_ON_GTE = ModelFields.CREATED_ON + '_Gte'
    CREATED_ON_LTE = ModelFields.CREATED_ON + '_Lte'
    UPDATED_ON = ModelFields.UPDATED_ON
    UPDATED_ON_GT = ModelFields.UPDATED_ON + '_Gt'
    UPDATED_ON_LT = ModelFields.UPDATED_ON + '_Lt'
    UPDATED_ON_GTE = ModelFields.UPDATED_ON + '_Gte'
    UPDATED_ON_LTE = ModelFields.UPDATED_ON + '_Lte'
