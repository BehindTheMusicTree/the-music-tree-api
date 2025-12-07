from api.model.spotify_resource.children.artist.Fields import Fields as ModelFields
from api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class Fields(PrivateUniqueResourceFields):
    NAME_PUBLIC = ModelFields.NAME
    POPULARITY_MIN = f'{ModelFields.POPULARITY}_min'
    POPULARITY_MAX = f'{ModelFields.POPULARITY}_max'
    CREATED_ON = ModelFields.CREATED_ON
    CREATED_ON_GT = f'{ModelFields.CREATED_ON}_gt'
    CREATED_ON_LT = f'{ModelFields.CREATED_ON}_lt'
    CREATED_ON_GTE = f'{ModelFields.CREATED_ON}_gte'
    CREATED_ON_LTE = f'{ModelFields.CREATED_ON}_lte'
    UPDATED_ON = ModelFields.UPDATED_ON
    UPDATED_ON_GT = f'{ModelFields.UPDATED_ON}_gt'
    UPDATED_ON_LT = f'{ModelFields.UPDATED_ON}_lt'
    UPDATED_ON_GTE = f'{ModelFields.UPDATED_ON}_gte'
    UPDATED_ON_LTE = f'{ModelFields.UPDATED_ON}_lte'
