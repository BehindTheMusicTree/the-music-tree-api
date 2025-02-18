from bodzify_api.model.ContentObjectFields import ContentObjectFields
from bodzify_api.model.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class Fields:
    CREATED_ON = PrivateUniqueResourceFields.CREATED_ON
    UPDATED_ON = PrivateUniqueResourceFields.UPDATED_ON
    USER = PrivateUniqueResourceFields.USER
    UUID = PrivateUniqueResourceFields.UUID

    CONTENT = ContentObjectFields.CONTENT
    CONTENT_TYPE = ContentObjectFields.CONTENT_TYPE
    CONTENT_UUID = ContentObjectFields.CONTENT_UUID
