from bodzify_api.model.private_standard_resource.Fields import Fields as PrivateRelationFields


class Fields:
    CREATED_ON = PrivateRelationFields.CREATED_ON
    UPDATED_ON = PrivateRelationFields.UPDATED_ON
    USER = PrivateRelationFields.USER
    DESCENDANT = 'descendant'
    ASCENDANT = 'ascendant'
    DEGREE = "degree"
