from bodzify_api.model.ContentObjectFields import ContentObjectFields
from bodzify_api.model.private_unique_resource.Fields import \
    Fields as PrivateUniqueResourceFields


class Fields(PrivateUniqueResourceFields, ContentObjectFields):
    pass
