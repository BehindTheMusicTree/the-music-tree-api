from bodzify_api.model.private.Fields import Fields as PrivateFields
from bodzify_api.model.public_standard_resource.Fields import Fields as PublicRelationFields
from bodzify_api.model.uuid.Fields import Fields as UuidFields


class Fields(PublicRelationFields, PrivateFields, UuidFields):
    pass
