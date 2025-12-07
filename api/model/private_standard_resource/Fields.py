from api.model.private.Fields import Fields as PrivateFields
from api.model.public_standard_resource.Fields import Fields as PublicStandardResourceFields


class Fields(PublicStandardResourceFields, PrivateFields):
    pass
