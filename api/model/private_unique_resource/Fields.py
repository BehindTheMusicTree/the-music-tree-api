from api.model.private.Fields import Fields as PrivateFields
from api.model.public_standard_resource.Fields import Fields as PublicRelationFields
from api.model.uuid.Fields import Fields as UuidFields


class Fields(PublicRelationFields, PrivateFields, UuidFields):
    pass
