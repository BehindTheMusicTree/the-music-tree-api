from bodzify_api.model.private.Fields import Fields as PrivateFields
from bodzify_api.model.public_standard_resource.Fields import     Fields as PublicRelationFields
from bodzify_api.model.uuid.Fields import Fields as UuidFields


class Fields:
    CREATED_ON = PublicRelationFields.CREATED_ON
    UPDATED_ON = PublicRelationFields.UPDATED_ON
    USER = PrivateFields.USER
    UUID = UuidFields.UUID
