from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria


class Genre(Criteria):
    class Meta(Criteria.Meta):
        db_table = f'{settings.APP_NAME}_genre'
