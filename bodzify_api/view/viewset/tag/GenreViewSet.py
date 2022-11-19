#!/usr/bin/env python

from bodzify_api.view.viewset.tag.TagViewSet import TagViewSet
from bodzify_api.serializer.tag.TagSerializer import TagRequestSerializer
from bodzify_api.serializer.tag.TagSerializer import TagResponseSerializer
from bodzify_api.model.tag.Tag import Tag
from bodzify_api.model.tag.TagType import TagTypesLabels

NAME_FIELD = "name"
PARENT_FIELD = "parent"

class GenreViewSet(TagViewSet):
  def __init__(self, tagTypeLabel=TagTypesLabels.GENRE, **kwargs): 
    super(GenreViewSet,self).__init__(tagTypeLabel, **kwargs)