from bodzify_api.model.private.Fields import Fields as PrivateFields
from bodzify_api.model.public_standard_resource.Fields import Fields as PublicStandardResourceFields


class Fields(PublicStandardResourceFields, PrivateFields):
    pass
