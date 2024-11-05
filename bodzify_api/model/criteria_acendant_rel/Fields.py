from bodzify_api.model.base.PrivateStandardResource import Fields as PrivateRelationFields


class Fields:
    MODEL = "criteria_ascendant_relation"
    CREATED_ON = PrivateRelationFields.CREATED_ON
    UPDATED_ON = PrivateRelationFields.UPDATED_ON
    USER = PrivateRelationFields.USER
    DESCENDANT = 'descendant'
    ASCENDANT = 'ascendant'
    DEGREE = "degree"
