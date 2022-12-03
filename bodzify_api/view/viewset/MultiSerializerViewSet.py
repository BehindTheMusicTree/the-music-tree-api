from rest_framework import viewsets


class MultiSerializerViewSet(viewsets.ModelViewSet):
    serializers = { 
        'default': None,
    }


    def get_serializer_class(self):
            return self.serializers.get(self.action,
                        self.serializers['default'])